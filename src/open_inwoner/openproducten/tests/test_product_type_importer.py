from unittest.mock import MagicMock, patch
from uuid import uuid4

from django.test import TestCase

import open_inwoner.pdc.models as pdc_models
from open_inwoner.openproducten.producttypes_imports import ProductTypeImporter
from open_inwoner.pdc.tests.factories import (
    CategoryFactory,
    ProductConditionFactory,
    ProductFactory,
    TagFactory,
)

from ..api_models import BaseCategory
from .helpers import (
    _create_condition,
    _create_file,
    _create_file_object,
    _create_link,
    _create_product_type,
    _create_question,
    _create_tag,
    _create_tag_type,
)


class TestProductTypeImporter(TestCase):
    def setUp(self):
        self.client = MagicMock()
        self.client.get_image.return_value = None
        self.client.get_file.return_value = _create_file_object(b"mocked file")

    def test_update_or_create_tag_type(self):
        for create in (True, False):
            with self.subTest(
                "should create instance if uuid does not exist"
                if create
                else "should update instance if uuid exists"
            ):
                uuid = uuid4()

                if not create:
                    pdc_models.TagType.objects.create(
                        open_producten_uuid=uuid, name="abc"
                    )

                tag_type = _create_tag_type(uuid)

                importer = ProductTypeImporter(self.client)
                instance = importer._update_or_create_tag_type(tag_type)

                self.assertEqual(pdc_models.TagType.objects.count(), 1)
                self.assertEqual(instance.open_producten_uuid, uuid)
                self.assertEqual(instance.name, tag_type.name)

                # Subtest does not reset db
                pdc_models.TagType.objects.all().delete()

    def test_update_or_create_tag(self):
        for create in (True, False):
            with self.subTest(
                "should create instance if uuid does not exist"
                if create
                else "should update instance if uuid exists"
            ):
                tag_uuid = uuid4()

                if not create:
                    TagFactory.create(open_producten_uuid=tag_uuid, name="abc")

                tag = _create_tag(tag_uuid)

                importer = ProductTypeImporter(self.client)
                instance = importer._update_or_create_tag(tag)

                self.assertEqual(pdc_models.Tag.objects.count(), 1)
                self.assertEqual(instance.open_producten_uuid, tag_uuid)
                self.assertEqual(instance.name, tag.name)

                # Subtest does not reset db
                pdc_models.Tag.objects.all().delete()
                pdc_models.TagType.objects.all().delete()

    def test_update_or_create_condition(self):
        for create in (True, False):
            with self.subTest(
                "should create instance if uuid does not exist"
                if create
                else "should update instance if uuid exists"
            ):
                uuid = uuid4()

                if not create:
                    ProductConditionFactory(open_producten_uuid=uuid)

                condition = _create_condition(uuid)

                importer = ProductTypeImporter(self.client)
                instance = importer._update_or_create_condition(condition)

                self.assertEqual(pdc_models.ProductCondition.objects.count(), 1)
                self.assertEqual(instance.open_producten_uuid, uuid)
                self.assertEqual(instance.name, condition.name)

                # Subtest does not reset db
                pdc_models.ProductCondition.objects.all().delete()

    def test_update_or_create_link(self):
        for create in (True, False):
            with self.subTest(
                "should create instance if uuid does not exist"
                if create
                else "should update instance if uuid exists"
            ):
                uuid = uuid4()

                product = ProductFactory()

                if not create:
                    pdc_models.ProductLink.objects.create(
                        open_producten_uuid=uuid,
                        name="abc",
                        url="https://example.com",
                        product=product,
                    )

                link = _create_link(uuid)
                importer = ProductTypeImporter(self.client)
                importer._update_or_create_link(link, product)

                instance = pdc_models.ProductLink.objects.first()

                self.assertEqual(pdc_models.ProductLink.objects.count(), 1)
                self.assertEqual(instance.open_producten_uuid, uuid)
                self.assertEqual(instance.name, link.name)

                # Subtest does not reset db
                pdc_models.ProductLink.objects.all().delete()

    def test_update_or_create_file(self):
        for create in (True, False):
            with self.subTest(
                "should create instance if uuid does not exist"
                if create
                else "should update instance if uuid exists"
            ):
                uuid = uuid4()

                product = ProductFactory()

                if not create:
                    pdc_models.ProductFile.objects.create(
                        open_producten_uuid=uuid,
                        file=_create_file_object(b"initial file"),
                        product=product,
                    )

                file = _create_file(uuid)
                importer = ProductTypeImporter(self.client)
                importer._update_or_create_file(file, product)

                instance = pdc_models.ProductFile.objects.first()

                self.assertEqual(pdc_models.ProductFile.objects.count(), 1)
                self.assertEqual(instance.open_producten_uuid, uuid)

                # Subtest does not reset db
                pdc_models.ProductFile.objects.all().delete()

    def test_update_or_create_product_type(self):
        for create in (True, False):
            with self.subTest(
                "should create instance if uuid does not exist"
                if create
                else "should update instance if uuid exists"
            ):
                uuid = uuid4()

                if not create:
                    ProductFactory.create(open_producten_uuid=uuid)

                product_type = _create_product_type(uuid)

                importer = ProductTypeImporter(self.client)
                instance = importer._update_or_create_product_type(product_type)

                self.assertEqual(pdc_models.Product.objects.count(), 1)
                self.assertEqual(instance.open_producten_uuid, uuid)
                self.assertEqual(instance.name, product_type.name)

                # Subtest does not reset db
                pdc_models.Product.objects.all().delete()

    def test_update_or_create_question(self):
        for create in (True, False):
            with self.subTest(
                "should create instance if uuid does not exist"
                if create
                else "should update instance if uuid exists"
            ):
                uuid = uuid4()

                product = ProductFactory()

                if not create:
                    pdc_models.Question.objects.create(
                        open_producten_uuid=uuid,
                        question="?",
                        answer="b",
                        product=product,
                    )

                question = _create_question(uuid)

                importer = ProductTypeImporter(self.client)
                importer._update_or_create_question(question, product)

                instance = pdc_models.Question.objects.first()

                self.assertEqual(pdc_models.Question.objects.count(), 1)
                self.assertEqual(instance.open_producten_uuid, uuid)
                self.assertEqual(instance.question, question.question)

                # Subtest does not reset db
                pdc_models.Question.objects.all().delete()

    def test_handle_relations_adds_adds_all_relations_to_product_type(self):
        product_type_uuid = uuid4()
        category_uuid = uuid4()

        tag = _create_tag(uuid4())
        condition = _create_condition(uuid4())

        link = _create_link(uuid4())
        question = _create_question(uuid4())
        file = _create_file(uuid4())

        product_type_instance = ProductFactory.create(
            open_producten_uuid=product_type_uuid
        )
        CategoryFactory.create(open_producten_uuid=category_uuid)

        product_type = _create_product_type(product_type_uuid)
        product_type.tags = [tag]
        product_type.conditions = [condition]
        product_type.categories = [BaseCategory(id=category_uuid)]
        product_type.links = [link]
        product_type.questions = [question]
        product_type.files = [file]

        importer = ProductTypeImporter(self.client)
        importer._handle_relations(product_type, product_type_instance)
        product_type_instance.save()

        self.assertEqual(product_type_instance.tags.first().open_producten_uuid, tag.id)
        self.assertEqual(
            product_type_instance.conditions.first().open_producten_uuid, condition.id
        )
        self.assertEqual(
            product_type_instance.categories.first().open_producten_uuid, category_uuid
        )
        self.assertEqual(
            product_type_instance.links.first().open_producten_uuid, link.id
        )
        self.assertEqual(
            product_type_instance.question_set.first().open_producten_uuid, question.id
        )
        self.assertEqual(
            product_type_instance.files.first().open_producten_uuid, file.id
        )

    @patch(
        "open_inwoner.openproducten.producttypes_imports.ProductTypeImporter._handle_product_type"
    )
    def test_handle_related_product_types_where_related_type_has_not_been_handled(
        self, mock_handle_product_type
    ):
        related_type_uuid = uuid4()

        ProductFactory(open_producten_uuid=related_type_uuid)
        product_type_instance = ProductFactory.create(open_producten_uuid=uuid4())
        related_product_type = _create_product_type(related_type_uuid)

        importer = ProductTypeImporter(self.client)
        importer.product_types = [related_product_type]
        importer._handle_related_product_types(
            [related_product_type.id], product_type_instance
        )

        mock_handle_product_type.assert_called_once()

    @patch(
        "open_inwoner.openproducten.producttypes_imports.ProductTypeImporter._handle_product_type"
    )
    def test_handle_related_product_types_where_related_type_has_been_handled(
        self, mock_handle_product_type
    ):
        related_type_uuid = uuid4()

        ProductFactory(open_producten_uuid=related_type_uuid)
        product_type_instance = ProductFactory.create(open_producten_uuid=uuid4())
        related_product_type = _create_product_type(related_type_uuid)

        importer = ProductTypeImporter(self.client)
        importer.product_types = [related_product_type]
        importer.handled_product_types = {
            related_product_type.id,
        }
        importer._handle_related_product_types(
            [related_product_type.id], product_type_instance
        )

        mock_handle_product_type.assert_not_called()

    @patch(
        "open_inwoner.openproducten.producttypes_imports.ProductTypeImporter._handle_relations"
    )
    @patch(
        "open_inwoner.openproducten.producttypes_imports.ProductTypeImporter._handle_related_product_types"
    )
    def test_handle_product_type_type_is_handled_when_not_in_handled_product_types(
        self, mock_handle_related_product_types, mock_handle_relations
    ):
        importer = ProductTypeImporter(self.client)

        product_type = _create_product_type(uuid4())
        importer._handle_product_type(product_type)

        mock_handle_related_product_types.assert_called_once()
        mock_handle_relations.assert_called_once()
        self.assertEqual(importer.handled_product_types, {product_type.id})

    @patch(
        "open_inwoner.openproducten.producttypes_imports.ProductTypeImporter._handle_relations"
    )
    @patch(
        "open_inwoner.openproducten.producttypes_imports.ProductTypeImporter._handle_related_product_types"
    )
    def test_handle_product_type_type_is_not_handled_when_in_handled_product_types(
        self, mock_handle_related_product_types, mock_handle_relations
    ):
        uuid = uuid4()

        importer = ProductTypeImporter(self.client)
        importer.handled_product_types = {uuid}
        product_type = _create_product_type(uuid)
        importer._handle_product_type(product_type)

        mock_handle_related_product_types.assert_not_called()
        mock_handle_relations.assert_not_called()

    def test_complete_import(self):  # TODO
        ...
