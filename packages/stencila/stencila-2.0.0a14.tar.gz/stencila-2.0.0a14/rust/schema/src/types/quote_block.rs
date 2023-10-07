// Generated file; do not edit. See `schema-gen` crate.

use crate::prelude::*;

use super::block::Block;
use super::cite_or_string::CiteOrString;
use super::string::String;

/// A section quoted from somewhere else.
#[skip_serializing_none]
#[derive(Debug, SmartDefault, Clone, PartialEq, Serialize, Deserialize, StripNode, HtmlCodec, JatsCodec, MarkdownCodec, TextCodec, ReadNode, WriteNode)]
#[serde(rename_all = "camelCase", crate = "common::serde")]
pub struct QuoteBlock {
    /// The type of this item
    pub r#type: MustBe!("QuoteBlock"),

    /// The identifier for this item
    #[strip(id)]
    #[html(attr = "id")]
    pub id: Option<String>,

    /// The source of the quote.
    pub cite: Option<CiteOrString>,

    /// The content of the quote.
    #[strip(types)]
    pub content: Vec<Block>,
}

impl QuoteBlock {
    pub fn new(content: Vec<Block>) -> Self {
        Self {
            content,
            ..Default::default()
        }
    }
}
