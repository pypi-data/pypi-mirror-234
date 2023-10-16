// Generated file; do not edit. See `schema-gen` crate.

use crate::prelude::*;

use super::execution_digest::ExecutionDigest;
use super::string::String;

/// A fragment of math, e.g a variable name, to be treated as inline content.
#[skip_serializing_none]
#[derive(Debug, SmartDefault, Clone, PartialEq, Serialize, Deserialize, StripNode, HtmlCodec, JatsCodec, MarkdownCodec, TextCodec, ReadNode, WriteNode)]
#[serde(rename_all = "camelCase", crate = "common::serde")]
#[html(elem = "math", custom)]
#[jats(elem = "inline-formula", special)]
#[markdown(special)]
pub struct MathFragment {
    /// The type of this item
    pub r#type: MustBe!("MathFragment"),

    /// The identifier for this item
    #[strip(id)]
    #[html(attr = "id")]
    pub id: Option<String>,

    /// The language used for the equation e.g tex, mathml, asciimath.
    pub math_language: String,

    /// The code of the equation in the `mathLanguage`.
    pub code: String,

    /// A digest of the `code` and `mathLanguage`.
    pub compile_digest: Option<ExecutionDigest>,

    /// Errors that occurred when parsing the math equation.
    pub errors: Option<Vec<String>>,

    /// The MathML transpiled from the `code`.
    #[html(content)]
    pub mathml: Option<String>,
}

impl MathFragment {
    pub fn new(math_language: String, code: String) -> Self {
        Self {
            math_language,
            code,
            ..Default::default()
        }
    }
}
