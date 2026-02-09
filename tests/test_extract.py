from osint_vortex_engine.extract import extract_entities


def test_extract_entities_basic():
    text = "Contact a@b.com https://x.y/z ip 1.2.3.4 @handle"
    ents = extract_entities(text)
    keys = {e.key() for e in ents}
    assert "email:a@b.com" in keys
    assert "ip:1.2.3.4" in keys
    assert "handle:@handle" in keys
    assert "domain:b.com" in keys
    assert any(k.startswith("url:") for k in keys)
