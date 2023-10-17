use crate::{value_eq, Comp};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::borrow::Borrow;
use std::collections::HashMap;
use std::fmt::{Display, Formatter};

/// A context captures the relevant state in which we want to find out whether a feature
/// should be available.
#[derive(Serialize, Deserialize, Debug, Clone, Default, PartialEq, Eq)]
pub struct Context {
    pub user_id: Option<String>,

    /// IETF language tag representing the preferred locale for the client, used for
    /// providing localized content. Consists of an ISO 639-1 primary language subtag and
    /// an optional ISO 3166-1 alpha-2 region subtag separated by an underscore.
    ///
    /// e.g. `en`, `en_US`.
    pub locale: Option<String>,

    /// A two-character ISO 3166-1 country code.
    ///
    /// e.g. `US`.
    pub country_code: Option<String>,
    pub device_id: Option<String>,
    pub canonical_url: Option<String>,
    pub subreddit_id: Option<String>,
    pub ad_account_id: Option<String>,
    pub business_id: Option<String>,
    pub origin_service: Option<String>,
    pub user_is_employee: Option<bool>,
    pub logged_in: Option<bool>,
    pub app_name: Option<String>,
    pub build_number: Option<i32>,
    pub oauth_client_id: Option<String>,
    pub cookie_created_timestamp: Option<i64>,

    /// A UUID, used to correlate events. Not used for targeting. If this value is present, and is a
    /// valid UUID, any events returned with decisions for this context will have their correlation
    /// id set to this value. If this value is not set or is not a valid UUID, [`Decider`] will
    /// generate and use a random v4 UUID.
    pub correlation_id: Option<String>,
    pub other_fields: Option<HashMap<String, Value>>,
}

impl Context {
    pub(super) fn cmp(&self, field: &ContextField, value: &Value) -> Option<bool> {
        field
            .get_value(self)
            .and_then(|other| value_eq(value, &other))
    }

    pub(super) fn cmp_op(&self, comp: Comp, field: &ContextField, rhs: f64) -> Option<bool> {
        // GT/LT and friends only really make sense on Numbers, but sometimes might
        // show up as Strings in the experiment_config.json
        self.field_to_float(field)
            .map(|lhs| comp.cmp_floats(lhs, rhs))
    }

    fn field_to_float(&self, field: &ContextField) -> Option<f64> {
        match field.get_value(self) {
            Some(Value::Number(n)) => n.as_f64(),
            Some(Value::String(s)) => s.parse::<f64>().ok(),
            _ => None,
        }
    }
}

/// `ContextField` provides a set of type-safe values for accessing fields inside a [`Context`].
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(from = "String", into = "String")]
pub enum ContextField {
    UserId,
    DeviceId,
    CanonicalUrl,
    SubredditId,
    AdAccountId,
    BusinessId,
    Locale,
    CountryCode,
    OriginService,
    AppName,
    UserIsEmployee,
    LoggedIn,
    BuildNumber,
    CookieCreatedTimestamp,
    OauthClientId,
    CorrelationId,
    Other(String),
}

impl ContextField {
    pub(super) fn get_value(&self, ctx: &Context) -> Option<Value> {
        match self {
            Self::UserId => ctx.user_id.as_deref().map(Value::from),
            Self::DeviceId => ctx.device_id.as_deref().map(Value::from),
            Self::CanonicalUrl => ctx.canonical_url.as_deref().map(Value::from),
            Self::SubredditId => ctx.subreddit_id.as_deref().map(Value::from),
            Self::AdAccountId => ctx.ad_account_id.as_deref().map(Value::from),
            Self::BusinessId => ctx.business_id.as_deref().map(Value::from),
            Self::Locale => ctx.locale.as_deref().map(Value::from),
            Self::CountryCode => ctx.country_code.as_deref().map(Value::from),
            Self::OriginService => ctx.origin_service.as_deref().map(Value::from),
            Self::AppName => ctx.app_name.as_deref().map(Value::from),
            Self::UserIsEmployee => ctx.user_is_employee.map(Value::from),
            Self::LoggedIn => ctx.logged_in.map(Value::from),
            Self::BuildNumber => ctx.build_number.map(Value::from),
            Self::CookieCreatedTimestamp => ctx.cookie_created_timestamp.map(Value::from),
            Self::OauthClientId => ctx.oauth_client_id.as_deref().map(Value::from),
            Self::CorrelationId => ctx.correlation_id.as_deref().map(Value::from),
            Self::Other(field) => ctx
                .other_fields
                .as_ref()
                .and_then(|hm| hm.get(field.as_str()).cloned()),
        }
    }
}

impl<T: Borrow<str>> From<T> for ContextField {
    fn from(sval: T) -> Self {
        match sval.borrow() {
            "user_id" => Self::UserId,
            "device_id" => Self::DeviceId,
            "canonical_url" => Self::CanonicalUrl,
            "subreddit_id" => Self::SubredditId,
            "ad_account_id" => Self::AdAccountId,
            "business_id" => Self::BusinessId,
            "locale" => Self::Locale,
            "country_code" => Self::CountryCode,
            "origin_service" => Self::OriginService,
            "app_name" => Self::AppName,
            "user_is_employee" => Self::UserIsEmployee,
            "logged_in" => Self::LoggedIn,
            "build_number" => Self::BuildNumber,
            "cookie_created_timestamp" => Self::CookieCreatedTimestamp,
            "oauth_client_id" => Self::OauthClientId,
            "correlation_id" => Self::CorrelationId,
            sval => Self::Other(sval.to_string()),
        }
    }
}

impl AsRef<str> for ContextField {
    fn as_ref(&self) -> &str {
        match self {
            Self::UserId => "user_id",
            Self::DeviceId => "device_id",
            Self::CanonicalUrl => "canonical_url",
            Self::SubredditId => "subreddit_id",
            Self::AdAccountId => "ad_account_id",
            Self::BusinessId => "business_id",
            Self::Locale => "locale",
            Self::CountryCode => "country_code",
            Self::OriginService => "origin_service",
            Self::AppName => "app_name",
            Self::UserIsEmployee => "user_is_employee",
            Self::LoggedIn => "logged_in",
            Self::BuildNumber => "build_number",
            Self::CookieCreatedTimestamp => "cookie_created_timestamp",
            Self::OauthClientId => "oauth_client_id",
            Self::CorrelationId => "correlation_id",
            Self::Other(field) => field.as_str(),
        }
    }
}

impl From<ContextField> for String {
    fn from(field: ContextField) -> Self {
        field.as_ref().to_string()
    }
}

impl Display for ContextField {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.as_ref())
    }
}

#[cfg(test)]
mod tests {
    pub(super) mod context_field {
        use super::super::ContextField;
        use proptest::prelude::*;
        use serde_json::Value;

        proptest! {
            #[test]
            fn test_from_string((field, tag) in context_field_strategy()) {
                let other = ContextField::from(tag.as_str());
                prop_assert_eq!(field, other);
            }

            #[test]
            fn test_serialize((field, tag) in context_field_strategy()) {
                let serialized = serde_json::to_value(&field).unwrap();
                prop_assert_eq!(Value::from(tag), serialized);
            }

            #[test]
            fn test_deserialize((field, tag) in context_field_strategy()) {
                let json_str = format!(r#""{}""#, tag);
                let deserialized: ContextField = serde_json::from_str(&json_str).unwrap();
                prop_assert_eq!(field, deserialized);
            }
        }

        pub(super) fn context_field_strategy() -> impl Strategy<Value = (ContextField, String)> {
            let other_strategy = "\\w+".prop_filter_map("got string with specific field", |s| {
                match ContextField::from(s.as_str()) {
                    cf @ ContextField::Other(_) => Some((cf, s)),
                    _ => None,
                }
            });

            prop_oneof![
                Just((ContextField::UserId, "user_id".to_string())),
                Just((ContextField::DeviceId, "device_id".to_string())),
                Just((ContextField::CanonicalUrl, "canonical_url".to_string())),
                Just((ContextField::SubredditId, "subreddit_id".to_string())),
                Just((ContextField::AdAccountId, "ad_account_id".to_string())),
                Just((ContextField::BusinessId, "business_id".to_string())),
                Just((ContextField::Locale, "locale".to_string())),
                Just((ContextField::CountryCode, "country_code".to_string())),
                Just((ContextField::OriginService, "origin_service".to_string())),
                Just((ContextField::AppName, "app_name".to_string())),
                Just((ContextField::UserIsEmployee, "user_is_employee".to_string())),
                Just((ContextField::LoggedIn, "logged_in".to_string())),
                Just((ContextField::BuildNumber, "build_number".to_string())),
                Just((
                    ContextField::CookieCreatedTimestamp,
                    "cookie_created_timestamp".to_string()
                )),
                Just((ContextField::OauthClientId, "oauth_client_id".to_string())),
                Just((ContextField::CorrelationId, "correlation_id".to_string())),
                other_strategy
            ]
        }
    }
}
