// Generated file; do not edit. See `schema-gen` crate.

use crate::prelude::*;

use super::list_item::ListItem;
use super::list_order::ListOrder;
use super::string::String;

/// A list of items.
#[skip_serializing_none]
#[derive(Debug, SmartDefault, Clone, PartialEq, Serialize, Deserialize, StripNode, HtmlCodec, JatsCodec, MarkdownCodec, TextCodec, ReadNode, WriteNode)]
#[serde(rename_all = "camelCase", crate = "common::serde")]
#[html(special)]
#[jats(elem = "list")]
#[markdown(special)]
pub struct List {
    /// The type of this item
    pub r#type: MustBe!("List"),

    /// The identifier for this item
    #[strip(id)]
    #[html(attr = "id")]
    pub id: Option<String>,

    /// The items in the list.
    #[jats(content)]
    pub items: Vec<ListItem>,

    /// The ordering of the list.
    #[jats(attr = "list-type")]
    pub order: ListOrder,
}

impl List {
    pub fn new(items: Vec<ListItem>, order: ListOrder) -> Self {
        Self {
            items,
            order,
            ..Default::default()
        }
    }
}
