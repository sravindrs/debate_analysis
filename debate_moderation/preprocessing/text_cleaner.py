import re

class TextCleaner:
    def __init__(self):
        # Configuration for optional features
        self.config = {
            "lowercase": True,
            "expand_contractions": True,
            "remove_fillers": True,
            "preserve_punctuation": True,
            "detect_questions": True,
            "detect_exclamations": True
        }

        # Filler words
        self.filler_words = ["um", "uh", "ah", "oh", "like", "you know", "actually", "basically", "frankly", "honestly"]

        # Contraction mapping
        self.contractions = {
            "ain't": "am not",
            "aren't": "are not",
            "can't": "cannot",
            "couldn't": "could not",
            "didn't": "did not",
            "doesn't": "does not",
            "don't": "do not",
            "hadn't": "had not",
            "hasn't": "has not",
            "haven't": "have not",
        }

        # Keywords for features
        self.negations = {'not', 'never', 'no', "don't", "won't", "can't"}
        self.references = {'you', 'he', 'she', 'they', 'him', 'her'}
        self.agreement_words = {'agree', 'exactly', 'right', 'absolutely', 'definitely'}
        self.disagreement_words = {'no', 'not', 'wrong', 'disagree', 'never', 'impossible'}
        self.emotion_words = {'happy', 'angry', 'sad', 'furious', 'frustrated', 'excited'}
        self.personal_attacks = {'liar', 'stupid', 'ignorant', 'dumb', 'fool', 'clueless'}
        self.group_identity = {'we', 'us', 'they', 'them'}
        self.emphasis_words = {'absolutely', 'really', 'very', 'totally', 'completely'}
        self.conditionals = {'if', 'unless', 'otherwise', 'in case'}

    ### --- Text Cleaning Methods ---
    def clean_text(self, text: str) -> str:
        """
        Cleans text by removing special characters and converting to lowercase.
        """
        if self.config["lowercase"]:
            text = text.lower()
        if self.config["expand_contractions"]:
            text = self._expand_contractions(text)
        if self.config["remove_fillers"]:
            text = self._remove_fillers(text)

        # Normalize spaces and remove non-ASCII characters
        text = re.sub(r'[^\x00-\x7F]+', ' ', text) 
        text = re.sub(r'\s+', ' ', text).strip()

        # Preserve punctuation or remove it based on config
        if not self.config["preserve_punctuation"]:
            text = re.sub(r'[^\w\s]', '', text) 

        return text
    
    def _expand_contractions(self, text: str) -> str:
        for contraction, expansion in self.contractions.items():
            text = re.sub(r'\b' + contraction + r'\b', expansion, text)
        return text
    
    def _remove_fillers(self, text: str) -> str:
        for filler in self.filler_words:
            text = re.sub(r'\b' + filler + r'\b', '', text)
        return text

    ### --- Feature Extraction Methods ---
    def is_question(self, text: str) -> bool:
        """Detects if the text ends with a question mark."""
        return text.endswith('?')
    
    def is_exclamation(self, text: str) -> bool:
        """Detects if the text ends with an exclamation mark."""
        return text.endswith('!')
    
    def is_statement(self, text: str) -> bool:
        """Detects if the text is a statement (not a question or exclamation)."""
        return not self.is_question(text) and not self.is_exclamation(text)
    
    def contains_negation(self, text: str) -> bool:
        """Detects negation words."""
        words = set(text.split())
        return bool(words & self.negations)
    
    def contains_reference(self, text: str) -> bool:
        """Detects references to other speakers."""
        words = set(text.split())
        return bool(words & self.references)

    def contains_agreement(self, text: str) -> bool:
        """Detects agreement words."""
        words = set(text.split())
        return bool(words & self.agreement_words)

    def contains_disagreement(self, text: str) -> bool:
        """Detects disagreement words."""
        words = set(text.split())
        return bool(words & self.disagreement_words)

    def contains_emotion_words(self, text: str) -> bool:
        """Detects emotion-related words."""
        words = set(text.split())
        return bool(words & self.emotion_words)

    def contains_personal_attack(self, text: str) -> bool:
        """Detects personal attacks."""
        words = set(text.split())
        return bool(words & self.personal_attacks)

    def contains_group_identity(self, text: str) -> bool:
        """Detects group identity language ('we', 'us', 'they')."""
        words = set(text.split())
        return bool(words & self.group_identity)

    def contains_emphasis(self, text: str) -> bool:
        """Detects emphasis words."""
        words = set(text.split())
        return bool(words & self.emphasis_words)

    def contains_conditional(self, text: str) -> bool:
        """Detects conditional words."""
        words = set(text.split())
        return bool(words & self.conditionals)

    def sentence_length(self, text: str) -> int:
        """Calculates sentence length based on word count."""
        return len(text.split())
