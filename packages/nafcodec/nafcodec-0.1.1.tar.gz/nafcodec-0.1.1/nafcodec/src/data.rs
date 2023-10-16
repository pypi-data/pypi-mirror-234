//! Common data types for this crate.

#[derive(Debug, Clone, PartialEq)]
pub enum MaskUnit {
    Masked(u64),
    Unmasked(u64),
}

impl MaskUnit {
    pub fn as_u64(&self) -> u64 {
        match self {
            MaskUnit::Masked(n) => *n,
            MaskUnit::Unmasked(n) => *n,
        }
    }
}

#[derive(Debug, Clone)]
pub struct Record {
    pub id: Option<String>,
    pub comment: Option<String>,
    pub sequence: Option<String>,
    pub quality: Option<String>,
    pub length: Option<u64>,
}

#[derive(Debug, Clone, Copy, Default, PartialEq)]
pub enum FormatVersion {
    #[default]
    V1,
    V2,
}

/// The type of sequence stored in a Nucleotide Archive Format file.
#[derive(Debug, Clone, Copy, Default, PartialEq)]
pub enum SequenceType {
    #[default]
    Dna,
    Rna,
    Protein,
    Text,
}

impl SequenceType {
    /// Check whether the sequence type is a nucleotide type.
    #[inline]
    pub fn is_nucleotide(&self) -> bool {
        match self {
            Self::Dna | Self::Rna => true,
            Self::Protein | Self::Text => false,
        }
    }
}

#[derive(Debug, Clone, Default)]
pub struct Flags(u8);

impl Flags {
    pub fn new(value: u8) -> Self {
        Self(value)
    }

    pub fn has_quality(&self) -> bool {
        (self.0 & 0x1) != 0
    }

    pub fn has_sequence(&self) -> bool {
        (self.0 & 0x2) != 0
    }

    pub fn has_mask(&self) -> bool {
        (self.0 & 0x4) != 0
    }

    pub fn has_lengths(&self) -> bool {
        (self.0 & 0x8) != 0
    }

    pub fn has_comments(&self) -> bool {
        (self.0 & 0x10) != 0
    }

    pub fn has_ids(&self) -> bool {
        (self.0 & 0x20) != 0
    }

    pub fn has_title(&self) -> bool {
        (self.0 & 0x40) != 0
    }

    pub fn has_extended_format(&self) -> bool {
        (self.0 & 0x80) != 0
    }
}

#[derive(Debug, Default, Clone)]
pub struct Header {
    pub(crate) format_version: FormatVersion,
    pub(crate) sequence_type: SequenceType,
    pub(crate) flags: Flags,
    pub(crate) name_separator: char,
    pub(crate) line_length: u64,
    pub(crate) number_of_sequences: u64,
}

impl Header {
    pub fn flags(&self) -> &Flags {
        &self.flags
    }

    pub fn line_length(&self) -> u64 {
        self.line_length
    }

    pub fn name_separator(&self) -> char {
        self.name_separator
    }

    pub fn number_of_sequences(&self) -> u64 {
        self.number_of_sequences
    }

    pub fn sequence_type(&self) -> SequenceType {
        self.sequence_type
    }

    pub fn format_version(&self) -> FormatVersion {
        self.format_version
    }
}
