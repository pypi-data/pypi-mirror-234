#![warn(rust_2018_idioms)]
// `borrow_deref_ref` is tripping on a bunch of the _parameters_ to functions in this file.
// My hunch is that the pyo3 attribute macros are transforming these functions in a way that creates
// &*(&T) calls. This is ultimately fine, so let's just allow this lint here.
#![allow(clippy::borrow_deref_ref)]

use std::collections::HashMap;
use std::fmt;
use std::fs::File;
use std::io::BufReader;

use pyo3::create_exception;
use pyo3::exceptions::PyException;
use pyo3::prelude::*;
use pyo3::types::{IntoPyDict, PyDict};
use pythonize::pythonize;
use serde_json::Value;

use decider::Decider as RustDecider;
use decider::DeciderError as RustDeciderError;
use decider::DeciderInitError as RustDeciderInitError;
use decider::Decision as RustDecision;
use decider::{Context, ContextField};

#[pyclass]
pub struct PyDecider {
    decider: Option<RustDecider>,
    err: Option<PyDeciderError>,
}

#[pyclass]
pub struct PyContext {
    context: Context,
    err: Option<PyDeciderError>,
}

#[pymethods]
impl PyContext {
    pub fn inspect(&self) -> String {
        format!("err: {:#?} \ncontext: {:#?}", self.err, self.context)
    }

    pub fn err(&self) -> Option<String> {
        self.err.as_ref().map(|e| e.to_string())
    }
}

#[pyclass]
pub struct GetExperimentRes {
    val: Option<Py<PyAny>>,
    pub err: Option<PyDeciderError>,
}

#[pymethods]
impl GetExperimentRes {
    pub fn inspect(&self) -> String {
        format!("err: {:?}, val: {:?}", self.err, self.val)
    }

    pub fn val(&mut self) -> Option<Py<PyAny>> {
        self.val.clone()
    }

    pub fn err(&self) -> Option<String> {
        self.err.as_ref().map(|e| e.to_string())
    }
}

#[pyclass]
pub struct GetBoolRes {
    val: bool,
    err: Option<PyDeciderError>,
}

#[pymethods]
impl GetBoolRes {
    pub fn inspect(&self) -> String {
        format!("err: {:?}, val: {:?}", self.err, self.val)
    }

    pub fn val(&self) -> bool {
        self.val
    }

    pub fn err(&self) -> Option<String> {
        self.err.as_ref().map(|e| e.to_string())
    }
}

#[pyclass]
pub struct GetIntegerRes {
    val: i64,
    err: Option<PyDeciderError>,
}

#[pymethods]
impl GetIntegerRes {
    pub fn inspect(&self) -> String {
        format!("err: {:?}, val: {:?}", self.err, self.val)
    }

    pub fn val(&self) -> i64 {
        self.val
    }

    pub fn err(&self) -> Option<String> {
        self.err.as_ref().map(|e| e.to_string())
    }
}

#[pyclass]
pub struct GetFloatRes {
    val: f64,
    err: Option<PyDeciderError>,
}

#[pymethods]
impl GetFloatRes {
    pub fn inspect(&self) -> String {
        format!("err: {:?}, val: {:?}", self.err, self.val)
    }

    pub fn val(&self) -> f64 {
        self.val
    }

    pub fn err(&self) -> Option<String> {
        self.err.as_ref().map(|e| e.to_string())
    }
}

#[pyclass]
pub struct GetStringRes {
    val: String,
    err: Option<PyDeciderError>,
}

#[pymethods]
impl GetStringRes {
    pub fn inspect(&self) -> String {
        format!("err: {:?}, val: {:?}", self.err, self.val)
    }

    pub fn val(&self) -> String {
        self.val.clone()
    }

    pub fn err(&self) -> Option<String> {
        self.err.as_ref().map(|e| e.to_string())
    }
}

#[pyclass]
pub struct GetMapRes {
    val: Py<PyAny>,
    err: Option<PyDeciderError>,
}

#[pymethods]
impl GetMapRes {
    pub fn inspect(&self) -> String {
        format!("err: {:?}, val: {:?}", self.err, self.val)
    }

    pub fn val(&self) -> Py<PyAny> {
        self.val.clone()
    }

    pub fn err(&self) -> Option<String> {
        self.err.as_ref().map(|e| e.to_string())
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct PyDecision {
    decision: Option<RustDecision>,
    err: Option<PyDeciderError>,
}

#[pymethods]
impl PyDecision {
    pub fn inspect(&self) -> String {
        format!("err: {:?}, decision: {:?}", self.err, self.decision)
    }

    pub fn decision(&self) -> Option<String> {
        self.decision.as_ref().and_then(|d| d.variant_name.clone())
    }

    pub fn decision_dict(&self) -> HashMap<String, String> {
        match &self.decision {
            None => HashMap::new(),
            Some(d) => match &d.variant_name {
                None => HashMap::new(),
                Some(name) => {
                    let mut out = HashMap::new();

                    out.insert("name".to_string(), name.to_string());
                    out.insert("id".to_string(), d.feature_id.to_string());
                    out.insert("version".to_string(), d.feature_version.to_string());
                    out.insert("experimentName".to_string(), d.feature_name.to_string());

                    out
                }
            },
        }
    }

    pub fn value_dict(&self) -> HashMap<String, Py<PyAny>> {
        let gil = Python::acquire_gil();
        let py = gil.python();
        match &self.decision {
            None => HashMap::new(),
            Some(d) => {
                let mut out: HashMap<String, Py<PyAny>> = HashMap::new();

                out.insert("name".to_string(), d.feature_name.clone().into_py(py));
                out.insert(
                    "type".to_string(),
                    match &d.value_type {
                        Some(vt) => vt.to_string().into_py(py),
                        None => "".into_py(py),
                    },
                );
                out.insert(
                    "value".to_string(),
                    match pythonize(py, &d.value.clone()) {
                        Ok(val) => val,
                        Err(_) => "".into_py(py),
                    },
                );

                out
            }
        }
    }

    pub fn events(&self) -> Vec<String> {
        match &self.decision {
            None => vec![],
            Some(d) => d.event_data.clone(),
        }
    }

    pub fn err(&self) -> Option<String> {
        self.err.as_ref().map(|e| e.to_string())
    }
}

#[pyclass]
pub struct GetAllDecisionsRes {
    decisions: Option<HashMap<String, PyDecision>>,
    err: Option<PyDeciderError>,
}

#[pymethods]
impl GetAllDecisionsRes {
    pub fn inspect(&self) -> String {
        format!("err: {:?}, decisions: {:?}", self.err, self.decisions)
    }

    pub fn decisions(&self) -> Option<HashMap<String, PyDecision>> {
        self.decisions.as_ref().cloned()
    }

    pub fn err(&self) -> Option<String> {
        self.err.as_ref().map(|e| e.to_string())
    }
}

#[pymethods]
impl PyDecider {
    pub fn err(&self) -> Option<String> {
        self.err.as_ref().map(|e| e.to_string())
    }

    pub fn choose(
        &self,
        feature_name: &str,
        ctx: &PyContext,
        identifier_type: Option<&str>,
    ) -> Option<PyDecision> {
        match &self.decider {
            Some(decider) => {
                let bfo = identifier_type.map(ContextField::from);

                let choose_res = decider.choose(feature_name, &ctx.context, bfo);

                match choose_res {
                    Ok(res) => Some(PyDecision {
                        decision: Some(res),
                        err: None,
                    }),
                    Err(e) => Some(PyDecision {
                        decision: None,
                        err: Some(PyDeciderError::GenericError(e.to_string())),
                    }),
                }
            }
            None => Some(PyDecision {
                decision: None,
                err: Some(PyDeciderError::DeciderNotFound),
            }),
        }
    }

    pub fn choose_all(&self, ctx: &PyContext, identifier_type: Option<&str>) -> GetAllDecisionsRes {
        match &self.decider {
            None => GetAllDecisionsRes {
                decisions: None,
                err: Some(PyDeciderError::DeciderNotFound),
            },
            Some(decider) => {
                let bfo = identifier_type.map(ContextField::from);

                let choose_all_res = decider.choose_all(&ctx.context, bfo);
                let decisions = choose_all_res
                    .into_iter()
                    .map(|(key, value)| {
                        let decision = match value {
                            Ok(decision) => PyDecision {
                                decision: Some(decision),
                                err: None,
                            },
                            Err(err) => PyDecision {
                                decision: None,
                                err: Some(PyDeciderError::GenericError(err.to_string())),
                            },
                        };
                        (key, decision)
                    })
                    .collect();

                GetAllDecisionsRes {
                    decisions: Some(decisions),
                    err: None,
                }
            }
        }
    }

    pub fn get_experiment(&self, feature_name: &str) -> GetExperimentRes {
        match &self.decider {
            Some(decider) => match decider.feature_by_name(feature_name) {
                Ok(feature) => {
                    let gil = Python::acquire_gil();
                    let py = gil.python();
                    match pythonize(py, &decider::LegacyExperiment::from(feature)) {
                        Ok(pydict) => GetExperimentRes {
                            val: Some(pydict),
                            err: None,
                        },
                        Err(e) => GetExperimentRes {
                            val: None,
                            err: Some(PyDeciderError::GenericError(e.to_string())),
                        },
                    }
                }
                Err(e) => GetExperimentRes {
                    val: None,
                    err: Some(PyDeciderError::GenericError(e.to_string())),
                },
            },
            None => GetExperimentRes {
                val: None,
                err: Some(PyDeciderError::DeciderNotFound),
            },
        }
    }

    pub fn get_bool(&self, feature_name: &str, ctx: &PyContext) -> GetBoolRes {
        match &self.decider {
            Some(decider) => match decider.get_bool(feature_name, &ctx.context) {
                Ok(b) => GetBoolRes { val: b, err: None },
                Err(e) => GetBoolRes {
                    val: false,
                    err: Some(PyDeciderError::GenericError(e.to_string())),
                },
            },
            None => GetBoolRes {
                val: false,
                err: Some(PyDeciderError::DeciderNotFound),
            },
        }
    }

    pub fn get_int(&self, feature_name: &str, ctx: &PyContext) -> GetIntegerRes {
        match &self.decider {
            Some(decider) => match decider.get_int(feature_name, &ctx.context) {
                Ok(i) => GetIntegerRes { val: i, err: None },
                Err(e) => GetIntegerRes {
                    val: 0,
                    err: Some(PyDeciderError::GenericError(e.to_string())),
                },
            },
            None => GetIntegerRes {
                val: 0,
                err: Some(PyDeciderError::DeciderNotFound),
            },
        }
    }

    pub fn get_float(&self, feature_name: &str, ctx: &PyContext) -> GetFloatRes {
        match &self.decider {
            Some(decider) => match decider.get_float(feature_name, &ctx.context) {
                Ok(f) => GetFloatRes { val: f, err: None },
                Err(e) => GetFloatRes {
                    val: 0.0,
                    err: Some(PyDeciderError::GenericError(e.to_string())),
                },
            },
            None => GetFloatRes {
                val: 0.0,
                err: Some(PyDeciderError::DeciderNotFound),
            },
        }
    }

    pub fn get_string(&self, feature_name: &str, ctx: &PyContext) -> GetStringRes {
        match &self.decider {
            Some(decider) => match decider.get_string(feature_name, &ctx.context) {
                Ok(s) => GetStringRes { val: s, err: None },
                Err(e) => GetStringRes {
                    val: "".to_string(),
                    err: Some(PyDeciderError::GenericError(e.to_string())),
                },
            },
            None => GetStringRes {
                val: "".to_string(),
                err: Some(PyDeciderError::DeciderNotFound),
            },
        }
    }

    pub fn get_map(&self, feature_name: &str, ctx: &PyContext) -> GetMapRes {
        let gil = Python::acquire_gil();
        let py = gil.python();
        match &self.decider {
            Some(decider) => {
                let res = decider.get_map(feature_name, &ctx.context);
                match res {
                    Ok(val) => match pythonize(py, &val) {
                        Ok(pydict) => GetMapRes {
                            val: pydict,
                            err: None,
                        },
                        Err(e) => {
                            let pany: Py<PyAny> = PyDict::new(py).into();
                            GetMapRes {
                                val: pany,
                                err: Some(PyDeciderError::GenericError(e.to_string())),
                            }
                        }
                    },
                    Err(e) => {
                        let pany: Py<PyAny> = PyDict::new(py).into();
                        GetMapRes {
                            val: pany,
                            err: Some(PyDeciderError::GenericError(e.to_string())),
                        }
                    }
                }
            }
            None => {
                let pany: Py<PyAny> = PyDict::new(py).into();
                GetMapRes {
                    val: pany,
                    err: Some(PyDeciderError::DeciderNotFound),
                }
            }
        }
    }

    pub fn get_all_values(&self, ctx: &PyContext) -> GetAllDecisionsRes {
        match &self.decider {
            None => GetAllDecisionsRes {
                decisions: None,
                err: Some(PyDeciderError::DeciderNotFound),
            },
            Some(decider) => {
                let mut out: HashMap<String, PyDecision> = HashMap::new();
                let all_values_res = decider.get_all_values(&ctx.context);
                match all_values_res {
                    Ok(res) => {
                        for (k, v) in res.iter() {
                            let val = PyDecision {
                                decision: Some(v.clone()),
                                err: None,
                            };
                            out.insert(k.clone(), val);
                        }
                        GetAllDecisionsRes {
                            decisions: Some(out),
                            err: None,
                        }
                    }
                    Err(e) => GetAllDecisionsRes {
                        decisions: None,
                        err: Some(PyDeciderError::GenericError(e.to_string())),
                    },
                }
            }
        }
    }
}

#[pyfunction]
pub fn init(decisionmakers: &str, filename: &str) -> PyDecider {
    let res = File::open(filename)
        .map_err(RustDeciderInitError::from)
        .and_then(|file| {
            let br = BufReader::new(file);
            let config: Value = serde_json::from_reader(br).map_err(RustDeciderInitError::from)?;

            Ok(config)
        })
        .and_then(|config| RustDecider::with_decisionmakers(config, decisionmakers));

    match res {
        Ok(decider) => PyDecider {
            decider: Some(decider),
            err: None,
        },
        Err(e) => {
            let err_string = e.to_string();
            match e {
                RustDeciderInitError::PartialLoad(decider, err_map) => {
                    let feature_errs = err_map
                        .into_iter()
                        .map(|(feature_name, error)| format!(r#"'{feature_name}': {error}"#))
                        .collect::<Vec<String>>()
                        .join(", ");

                    PyDecider {
                        decider: Some(decider),
                        err: Some(PyDeciderError::DeciderInitFailed(format!(
                            r#"{err_string}: {{ {feature_errs} }}"#
                        ))),
                    }
                }
                _ => PyDecider {
                    decider: None,
                    err: Some(PyDeciderError::DeciderInitFailed(e.to_string())),
                },
            }
        }
    }
}

#[pyfunction]
pub fn make_ctx(ctx_dict: &PyDict) -> PyContext {
    let mut err_vec: Vec<String> = Vec::new();

    let user_id: Option<String> = match extract_field::<String>(ctx_dict, "user_id", "string") {
        Ok(u_id) => u_id,
        Err(e) => {
            err_vec.push(e);
            None
        }
    };

    let locale: Option<String> = match extract_field::<String>(ctx_dict, "locale", "string") {
        Ok(loc) => loc,
        Err(e) => {
            err_vec.push(e);
            None
        }
    };

    let device_id = match extract_field::<String>(ctx_dict, "device_id", "string") {
        Ok(d_id) => d_id,
        Err(e) => {
            err_vec.push(e);
            None
        }
    };

    let canonical_url = match extract_field::<String>(ctx_dict, "canonical_url", "string") {
        Ok(c_url) => c_url,
        Err(e) => {
            err_vec.push(e);
            None
        }
    };

    let subreddit_id: Option<String> =
        match extract_field::<String>(ctx_dict, "subreddit_id", "string") {
            Ok(s_id) => s_id,
            Err(e) => {
                err_vec.push(e);
                None
            }
        };

    let ad_account_id: Option<String> =
        match extract_field::<String>(ctx_dict, "ad_account_id", "string") {
            Ok(aa_id) => aa_id,
            Err(e) => {
                err_vec.push(e);
                None
            }
        };

    let business_id: Option<String> =
        match extract_field::<String>(ctx_dict, "business_id", "string") {
            Ok(ab_id) => ab_id,
            Err(e) => {
                err_vec.push(e);
                None
            }
        };

    let country_code = match extract_field::<String>(ctx_dict, "country_code", "string") {
        Ok(cc) => cc,
        Err(e) => {
            err_vec.push(e);
            None
        }
    };

    let origin_service = match extract_field::<String>(ctx_dict, "origin_service", "string") {
        Ok(os) => os,
        Err(e) => {
            err_vec.push(e);
            None
        }
    };

    let user_is_employee = match extract_field::<bool>(ctx_dict, "user_is_employee", "bool") {
        Ok(uie) => uie,
        Err(e) => {
            err_vec.push(e);
            None
        }
    };

    let logged_in = match extract_field::<bool>(ctx_dict, "logged_in", "bool") {
        Ok(li) => li,
        Err(e) => {
            err_vec.push(e);
            None
        }
    };

    let app_name = match extract_field::<String>(ctx_dict, "app_name", "string") {
        Ok(an) => an,
        Err(e) => {
            err_vec.push(e);
            None
        }
    };

    let build_number = match extract_field::<i32>(ctx_dict, "build_number", "integer") {
        Ok(bn) => bn,
        Err(e) => {
            err_vec.push(e);
            None
        }
    };

    let oauth_client_id = match extract_field::<String>(ctx_dict, "oauth_client_id", "string") {
        Ok(at) => at,
        Err(e) => {
            err_vec.push(e);
            None
        }
    };

    let cookie_created_timestamp =
        match extract_field::<i64>(ctx_dict, "cookie_created_timestamp", "integer") {
            Ok(cct) => cct,
            Err(e) => {
                err_vec.push(e);
                None
            }
        };

    let correlation_id = match extract_field::<String>(ctx_dict, "correlation_id", "string") {
        Ok(cid) => cid,
        Err(e) => {
            err_vec.push(e);
            None
        }
    };

    let other_fields = match extract_field::<HashMap<String, Option<OtherVal>>>(
        ctx_dict,
        "other_fields",
        "hashmap",
    ) {
        Ok(Some(ofm)) => {
            let mut out = HashMap::new();

            for (key, val) in ofm.iter() {
                let v: Value = match val {
                    None => Value::Null,
                    Some(OtherVal::B(b)) => Value::from(*b),
                    Some(OtherVal::I(i)) => Value::from(*i),
                    Some(OtherVal::F(f)) => Value::from(*f),
                    Some(OtherVal::S(s)) => Value::from(s.clone()),
                };
                if v != Value::Null {
                    out.insert(key.clone(), v);
                }
            }
            Some(out)
        }
        Ok(None) => None,
        Err(e) => {
            err_vec.push(e);
            None
        }
    };

    PyContext {
        context: Context {
            user_id,
            locale,
            device_id,
            canonical_url,
            subreddit_id,
            ad_account_id,
            business_id,
            country_code,
            origin_service,
            user_is_employee,
            logged_in,
            app_name,
            build_number,
            oauth_client_id,
            cookie_created_timestamp,
            correlation_id,
            other_fields,
        },
        err: match err_vec.len() {
            0 => None,
            _ => Some(PyDeciderError::GenericError(err_vec.join("\n"))),
        },
    }
}

fn extract_field<'p, T>(
    ctx_dict: &'p PyDict,
    key: &str,
    field_type: &str,
) -> Result<Option<T>, String>
where
    T: FromPyObject<'p>,
{
    match ctx_dict.get_item(key) {
        Some(val) => {
            if val.is_none() {
                Ok(None)
            } else {
                match val.extract::<T>() {
                    Ok(s) => Ok(Some(s)),
                    _ => Err(format!("{:#?} type mismatch ({:}).", key, field_type)),
                }
            }
        }
        None => Ok(None),
    }
}

#[derive(FromPyObject)]
enum OtherVal {
    B(bool),
    S(String),
    I(i64),
    F(f64),
}

#[derive(Debug, Clone)]
pub enum PyDeciderError {
    DeciderNotFound,
    GenericError(String),
    DeciderInitFailed(String),
}

impl fmt::Display for PyDeciderError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            PyDeciderError::DeciderNotFound => write!(f, "Decider not found."),
            PyDeciderError::DeciderInitFailed(e) => {
                write!(f, "Decider initialization failed: {:#}.", e)
            }
            PyDeciderError::GenericError(e) => {
                write!(f, "{}", e)
            }
        }
    }
}

// New Binding API

create_exception!(
    rust_decider,
    DeciderInitException,
    PyException,
    "Decider initialization failed."
);

create_exception!(
    rust_decider,
    PartialLoadException,
    DeciderInitException,
    "Decider partially loaded during initialization and contains errors."
);

create_exception!(
    rust_decider,
    DeciderException,
    PyException,
    "Decider API error."
);
create_exception!(
    rust_decider,
    FeatureNotFoundException,
    DeciderException,
    "Decider feature not found error."
);
create_exception!(
    rust_decider,
    ValueTypeMismatchException,
    DeciderException,
    "Value type mismatch."
);

#[pyclass]
pub struct Decider {
    decider: RustDecider,
}

#[pymethods]
impl Decider {
    #[new]
    fn new(path: &str) -> PyResult<Self> {
        match RustDecider::new(path) {
            Ok(decider) => Ok(Decider { decider }),
            Err(e) => {
                let err_string = e.to_string();
                match e {
                    RustDeciderInitError::PartialLoad(decider, err_map) => {
                        let py_errs: Py<PyDict> = Python::with_gil(|py| {
                            let errors = err_map
                                .into_iter()
                                .map(|(feature_name, err)| (feature_name, err.to_string()));

                            errors.into_py_dict(py).into_py(py)
                        });

                        Err(PartialLoadException::new_err((
                            err_string,
                            Decider { decider },
                            py_errs,
                        )))
                    }
                    _ => Err(DeciderInitException::new_err(format!(
                        r#"Decider initialization failed: {e}"#
                    ))),
                }
            }
        }
    }

    pub fn choose(&self, feature_name: &str, ctx: &PyContext) -> PyResult<Decision> {
        let choose_res = self.decider.choose(feature_name, &ctx.context, None);

        match choose_res {
            Ok(res) => Ok(res.into()),
            Err(err) => match err {
                RustDeciderError::FeatureNotFoundWithName(f) => Err(
                    FeatureNotFoundException::new_err(format!(r#"Feature "{f}" not found."#)),
                ),
                _ => Err(DeciderException::new_err(err.to_string())),
            },
        }
    }

    pub fn choose_all(
        &self,
        ctx: &PyContext,
        identifier_type: Option<&str>,
    ) -> HashMap<String, Decision> {
        let bfo = identifier_type.map(ContextField::from);

        let choose_all_res = self.decider.choose_all(&ctx.context, bfo);
        choose_all_res
            .into_iter()
            .filter_map(|(feature_name, decision_result)| match decision_result {
                Ok(decision) => Some((feature_name, decision.into())),
                _ => None,
            })
            .collect()
    }

    pub fn get_bool(&self, feature_name: &str, ctx: &PyContext) -> PyResult<bool> {
        self.decider
            .get_bool(feature_name, &ctx.context)
            .map_err(|err| match err {
                RustDeciderError::FeatureNotFoundWithName(f) => {
                    FeatureNotFoundException::new_err(format!(r#"Feature "{f}" not found."#))
                }
                RustDeciderError::DcTypeMismatch => ValueTypeMismatchException::new_err(format!(
                    r#"Feature "{feature_name}" not of boolean type."#
                )),
                _ => DeciderException::new_err(err.to_string()),
            })
    }

    pub fn get_int(&self, feature_name: &str, ctx: &PyContext) -> PyResult<i64> {
        self.decider
            .get_int(feature_name, &ctx.context)
            .map_err(|err| match err {
                RustDeciderError::FeatureNotFoundWithName(f) => {
                    FeatureNotFoundException::new_err(format!(r#"Feature "{f}" not found."#))
                }
                RustDeciderError::DcTypeMismatch => ValueTypeMismatchException::new_err(format!(
                    r#"Feature "{feature_name}" not of integer type."#
                )),
                _ => DeciderException::new_err(err.to_string()),
            })
    }

    pub fn get_float(&self, feature_name: &str, ctx: &PyContext) -> PyResult<f64> {
        self.decider
            .get_float(feature_name, &ctx.context)
            .map_err(|err| match err {
                RustDeciderError::FeatureNotFoundWithName(f) => {
                    FeatureNotFoundException::new_err(format!(r#"Feature "{f}" not found."#))
                }
                RustDeciderError::DcTypeMismatch => ValueTypeMismatchException::new_err(format!(
                    r#"Feature "{feature_name}" not of float type."#
                )),
                _ => DeciderException::new_err(err.to_string()),
            })
    }

    pub fn get_string(&self, feature_name: &str, ctx: &PyContext) -> PyResult<String> {
        self.decider
            .get_string(feature_name, &ctx.context)
            .map_err(|err| match err {
                RustDeciderError::FeatureNotFoundWithName(f) => {
                    FeatureNotFoundException::new_err(format!(r#"Feature "{f}" not found."#))
                }
                RustDeciderError::DcTypeMismatch => ValueTypeMismatchException::new_err(format!(
                    r#"Feature "{feature_name}" not of string type."#
                )),
                _ => DeciderException::new_err(err.to_string()),
            })
    }

    pub fn get_map(&self, feature_name: &str, ctx: &PyContext) -> PyResult<Py<PyDict>> {
        match self.decider.get_map(feature_name, &ctx.context) {
            Ok(m) => Python::with_gil(|py| {
                Ok(m.iter()
                    // Map values using the extension trait.
                    .map(|(key, value)| (key, value.to_py_object(py)))
                    // Turn the resulting iterator into a dict.
                    .into_py_dict(py)
                    .into_py(py))
            }),
            Err(err) => match err {
                RustDeciderError::FeatureNotFoundWithName(f) => Err(
                    FeatureNotFoundException::new_err(format!(r#"Feature "{f}" not found."#)),
                ),
                RustDeciderError::DcTypeMismatch => Err(ValueTypeMismatchException::new_err(
                    format!(r#"Feature "{feature_name}" not of map type."#),
                )),
                _ => Err(DeciderException::new_err(err.to_string())),
            },
        }
    }

    pub fn all_values(&self, ctx: &PyContext) -> HashMap<String, Decision> {
        let all_values_res = self
            .decider
            .get_all_values(&ctx.context)
            .expect("get_all_values is infallible");
        all_values_res
            .into_iter()
            .map(|(feature_name, decision)| (feature_name, decision.into()))
            .collect()
    }

    pub fn get_feature(&self, feature_name: &str) -> PyResult<Feature> {
        match self.decider.feature_by_name(feature_name) {
            Ok(feature) => Ok(feature.into()),
            Err(err) => match err {
                RustDeciderError::FeatureNotFoundWithName(f) => Err(
                    FeatureNotFoundException::new_err(format!(r#"Feature "{f}" not found."#)),
                ),
                _ => Err(DeciderException::new_err(err.to_string())),
            },
        }
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct Decision {
    #[pyo3(get)]
    pub variant_name: Option<String>,
    #[pyo3(get)]
    pub feature_id: u32,
    #[pyo3(get)]
    pub feature_name: String,
    #[pyo3(get)]
    pub feature_version: u32,
    #[pyo3(get)]
    pub value: Py<PyAny>,
    #[pyo3(get)]
    pub value_type: Option<String>,
    #[pyo3(get)]
    // TODO Remove event_data once we've migrated off of the legacy string format.
    pub event_data: Vec<String>,
    // #[pyo3(get)]
    // pub events: Vec<Event>,
}

impl From<decider::Decision> for Decision {
    fn from(d: decider::Decision) -> Self {
        Python::with_gil(|py| {
            Decision {
                variant_name: d.variant_name.clone(),
                feature_id: d.feature_id,
                feature_name: d.feature_name.clone(),
                feature_version: d.feature_version,
                value: match pythonize(py, &d.value) {
                    Ok(val) => val,
                    Err(_) => py.None(),
                },
                value_type: d.value_type.map(|vt| vt.to_string()),
                event_data: d.event_data.clone(),
                // TODO:
                // events: id.events,
            }
        })
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct Feature {
    #[pyo3(get)]
    pub id: u32,
    #[pyo3(get)]
    pub version: u32,
    #[pyo3(get)]
    pub name: String,
    #[pyo3(get)]
    pub bucket_val: String,
    #[pyo3(get)]
    pub start_ts: u64,
    #[pyo3(get)]
    pub stop_ts: u64,
    #[pyo3(get)]
    pub owner: String,
    #[pyo3(get)]
    pub emit_event: bool,
}

impl From<&decider::Feature> for Feature {
    fn from(f: &decider::Feature) -> Self {
        let (vs_ref, emit_event) = match f {
            decider::Feature::RangeVariant(rv) => (Some(&rv.variant_set), rv.emit_event),
            _ => (None, false),
        };

        Feature {
            id: f.metadata().id,
            version: f.metadata().version,
            name: f.metadata().name.clone(),
            bucket_val: vs_ref
                .map(|vs| vs.bucketing_field.as_ref().to_string())
                .unwrap_or_default(),
            start_ts: vs_ref.map(|vs| vs.start_ts).unwrap_or_default(),
            stop_ts: vs_ref.map(|vs| vs.stop_ts).unwrap_or_default(),
            owner: f.metadata().owner.clone(),
            emit_event,
        }
    }
}

trait ValuePyObjectExt {
    fn to_py_object(&self, py: Python<'_>) -> PyObject;
}

impl ValuePyObjectExt for Value {
    fn to_py_object(&self, py: Python<'_>) -> PyObject {
        match self {
            // null turns into None
            Value::Null => py.None(),
            Value::Bool(b) => b.to_object(py),
            // All JSON numbers are floats so we keep them floats.
            Value::Number(num) => num
                .as_f64()
                .expect("finite-precision floats are infallible")
                .to_object(py),
            Value::String(s) => s.to_object(py),
            // JSON arrays recursively store JSON objects. This branch uses this trait to turn the
            // inner Vec into a Vec of python objects.
            Value::Array(arr) => arr
                .iter()
                .map(|value| value.to_py_object(py))
                .collect::<Vec<_>>()
                .to_object(py),
            // Objects are the same idea as arrays, but we need to turn the map into a dict first.
            Value::Object(obj) => obj
                .iter()
                .map(|(key, value)| (key, value.to_py_object(py)))
                .into_py_dict(py)
                .to_object(py),
        }
    }
}

#[pyfunction]
pub const fn version() -> &'static str {
    env!("CARGO_PKG_VERSION")
}

#[pymodule]
fn rust_decider(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(init, m)?)?;
    m.add_function(wrap_pyfunction!(make_ctx, m)?)?;
    m.add_function(wrap_pyfunction!(version, m)?)?;
    m.add("DeciderException", py.get_type::<DeciderException>())?;
    m.add(
        "DeciderInitException",
        py.get_type::<DeciderInitException>(),
    )?;
    m.add(
        "PartialLoadException",
        py.get_type::<PartialLoadException>(),
    )?;
    m.add(
        "FeatureNotFoundException",
        py.get_type::<FeatureNotFoundException>(),
    )?;
    m.add(
        "ValueTypeMismatchException",
        py.get_type::<ValueTypeMismatchException>(),
    )?;
    m.add_class::<Decider>()?;

    Ok(())
}
