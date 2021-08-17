#
# This file is part of Land Cover Classification System Database Model.
# Copyright (C) 2021 INPE.
#
# Land Cover Classification System Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Unit-test for models of LCCS-DB."""
import pytest

from lccs_db import LCCSDatabase
from lccs_db.models import LucClassificationSystem, ClassificationSystemSRC


from sqlalchemy_utils import i18n, TranslationHybrid  # noqa


@pytest.fixture
def translation_hybrid():
    return TranslationHybrid('pt-br', 'en')


@pytest.fixture
def db(app):
    ext = LCCSDatabase(app)

    yield ext.db


@pytest.fixture
def test_classification_system():
    """Test create a classification system."""
    system = LucClassificationSystem(
        name="Classification-System-Test",
        authority_name="BDC",
        description="Description",
        version="1.0"
    )
    with db.session.begin_nested():
        db.session.add(system)
        db.session.commit()

    assert system.id


@pytest.fixture
def test_using_hybrid_as_constructor():
    system = LucClassificationSystem(name='Classification-System-Test')
    assert system.name_translations['pt-br'] == 'Classification-System-Test'


@pytest.fixture
def test_hybrid_property():
    system = LucClassificationSystem(name='System-Test', version=1)
    assert system.identifier == 'System-Test-1'


@pytest.fixture
def test_if_no_translation_exists_returns_none():
    system = LucClassificationSystem()
    assert system.name is None


@pytest.mark.parametrize(
        ('title_translations', 'name', 'authority_name', 'version'),
        (
            ({'pt-br': 'teste-uct', 'en': 'test-uct'}, 'uct', 'LULC', 1),
            ({'pt-br': 'teste-uct'}, 'uct', 'LULC', 2),
            ({'en': 'test-uct'}, 'uct', 'LULC', 3)
        )
)
@pytest.fixture
def test_hybrid_as_an_expression(title_translations, name, authority_name, version):
    system = LucClassificationSystem(title_translations=title_translations,
                                     name=name,
                                     authority_name=authority_name,
                                     version=version)
    with db.session.begin_nested():
        db.session.add(system)
    db.session.commit()

    assert db.session.query(LucClassificationSystem.name) == name


@pytest.fixture
def test_classification_system_srs():
    """Test create a classification system."""
    system = LucClassificationSystem(
        name="Classification-System-Test",
        authority_name="BDC",
        description="Description",
        version="1.0"
    )
    system_t = LucClassificationSystem(
        name="Classification-System-Test",
        authority_name="BDC",
        description="Description",
        version="2.0"
    )

    with db.session.begin_nested():
        db.session.add(system)
        db.session.add(system_t)
        db.session.commit()

    src = ClassificationSystemSRC(classification_system_id=system_t.id, classification_system_src_id=system.id)

    assert src.classification_system_id == system_t.id
    assert src.classification_system_src_id == system.id
