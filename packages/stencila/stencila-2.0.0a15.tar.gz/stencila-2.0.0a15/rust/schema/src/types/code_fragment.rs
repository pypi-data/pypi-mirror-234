// Generated file; do not edit. See `schema-gen` crate.

use crate::prelude::*;

use super::cord::Cord;
use super::string::String;

/// Inline code.
#[skip_serializing_none]
#[derive(Debug, SmartDefault, Clone, PartialEq, Serialize, Deserialize, StripNode, HtmlCodec, JatsCodec, MarkdownCodec, TextCodec, ReadNode, WriteNode)]
#[serde(rename_all = "camelCase", crate = "common::serde")]
#[html(elem = "code", custom)]
#[jats(elem = "monospace", attribs(specific__use = "code"))]
#[markdown(special)]
pub struct CodeFragment {
    /// The type of this item
    pub r#type: MustBe!("CodeFragment"),

    /// The identifier for this item
    #[strip(id)]
    #[html(attr = "id")]
    pub id: Option<String>,

    /// The code.
    #[html(content)]
    #[jats(content)]
    pub code: Cord,

    /// The programming language of the code.
    #[jats(attr = "language")]
    pub programming_language: Option<String>,
}

impl CodeFragment {
    pub fn new(code: Cord) -> Self {
        Self {
            code,
            ..Default::default()
        }
    }
}
