// Generated file; do not edit. See `schema-gen` crate.

use crate::prelude::*;

use super::block::Block;
use super::note_type::NoteType;
use super::string::String;

/// Additional content which is not part of the main content of a document.
#[skip_serializing_none]
#[derive(Debug, SmartDefault, Clone, PartialEq, Serialize, Deserialize, StripNode, HtmlCodec, JatsCodec, MarkdownCodec, TextCodec, ReadNode, WriteNode)]
#[serde(rename_all = "camelCase", crate = "common::serde")]
pub struct Note {
    /// The type of this item
    pub r#type: MustBe!("Note"),

    /// The identifier for this item
    #[strip(id)]
    #[html(attr = "id")]
    pub id: Option<String>,

    /// Determines where the note content is displayed within the document.
    pub note_type: NoteType,

    /// Content of the note, usually a paragraph.
    #[strip(types)]
    pub content: Vec<Block>,
}

impl Note {
    pub fn new(note_type: NoteType, content: Vec<Block>) -> Self {
        Self {
            note_type,
            content,
            ..Default::default()
        }
    }
}
