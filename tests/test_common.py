from local_rag_qa.common import chunk_text, cosine_similarity


def test_chunk_text_splits_on_blank_lines():
    text = "First paragraph is long enough.\n\nSecond paragraph is also long enough."
    assert chunk_text(text) == [
        "First paragraph is long enough.",
        "Second paragraph is also long enough.",
    ]


def test_chunk_text_drops_short_fragments():
    text = (
        "This paragraph is long enough to survive.\n\n"
        "short\n\n"
        "Another long enough paragraph goes here."
    )
    chunks = chunk_text(text)
    assert "short" not in chunks
    assert len(chunks) == 2


def test_chunk_text_strips_whitespace():
    text = "  \n\n  Padded paragraph text goes right here.  \n\n  "
    assert chunk_text(text) == ["Padded paragraph text goes right here."]


def test_chunk_text_empty_input_returns_no_chunks():
    assert chunk_text("") == []
    assert chunk_text("   \n\n  ") == []


def test_cosine_similarity_identical_vectors_is_one():
    a = [1.0, 2.0, 3.0]
    assert cosine_similarity(a, a) == 1.0


def test_cosine_similarity_orthogonal_vectors_is_zero():
    assert cosine_similarity([1.0, 0.0], [0.0, 1.0]) == 0.0


def test_cosine_similarity_opposite_vectors_is_minus_one():
    assert cosine_similarity([1.0, 0.0], [-1.0, 0.0]) == -1.0


def test_cosine_similarity_zero_vector_returns_zero():
    assert cosine_similarity([0.0, 0.0], [1.0, 1.0]) == 0.0
