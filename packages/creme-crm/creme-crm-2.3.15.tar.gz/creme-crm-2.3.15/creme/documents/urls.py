# -*- coding: utf-8 -*-

from django.urls import re_path

from creme import documents
from creme.creme_core.conf.urls import Swappable, swap_manager

from .views import document, folder, quick_forms

urlpatterns = [
    *swap_manager.add_group(
        documents.folder_model_is_custom,
        Swappable(
            re_path(
                r'^folders[/]?$',
                folder.FoldersList.as_view(),
                name='documents__list_folders',
            ),
        ),
        Swappable(
            re_path(
                r'^folder/add[/]?$',
                folder.FolderCreation.as_view(),
                name='documents__create_folder',
            ),
        ),
        Swappable(
            re_path(
                r'^folder/(?P<parent_id>\d+)/add/child[/]?$',
                folder.ChildFolderCreation.as_view(),
                name='documents__create_folder',
            ),
            check_args=Swappable.INT_ID,
        ),
        Swappable(
            re_path(
                r'^folder/(?P<folder_id>\d+)/add/child/popup[/]?$',
                folder.ChildFolderCreationPopup.as_view(),
                name='documents__create_child_folder',
            ),
            check_args=Swappable.INT_ID,
        ),
        Swappable(
            re_path(
                r'^folder/edit/(?P<folder_id>\d+)[/]?$',
                folder.FolderEdition.as_view(),
                name='documents__edit_folder',
            ),
            check_args=Swappable.INT_ID,
        ),
        Swappable(
            re_path(
                r'^folder/(?P<folder_id>\d+)[/]?$',
                folder.FolderDetail.as_view(),
                name='documents__view_folder',
            ),
            check_args=Swappable.INT_ID,
        ),
        app_name='documents',
    ).kept_patterns(),

    *swap_manager.add_group(
        documents.document_model_is_custom,
        Swappable(
            re_path(
                r'^documents[/]?$',
                document.DocumentsList.as_view(),
                name='documents__list_documents')),
        Swappable(
            re_path(
                r'^document/add[/]?$',
                document.DocumentCreation.as_view(),
                name='documents__create_document',
            ),
        ),
        Swappable(
            re_path(
                r'^document/add_related/(?P<entity_id>\d+)[/]?',
                document.RelatedDocumentCreation.as_view(),
                name='documents__create_related_document',
            ),
            check_args=Swappable.INT_ID,
        ),
        Swappable(
            re_path(
                r'^document/edit/(?P<document_id>\d+)[/]?$',
                document.DocumentEdition.as_view(),
                name='documents__edit_document',
            ),
            check_args=Swappable.INT_ID,
        ),
        Swappable(
            re_path(
                r'^document/(?P<document_id>\d+)[/]?$',
                document.DocumentDetail.as_view(),
                name='documents__view_document',
            ),
            check_args=Swappable.INT_ID,
        ),

        Swappable(
            re_path(
                r'^quickforms/from_widget/document/csv/add[/]?$',
                quick_forms.QuickDocumentCreation.as_view(),
                name='documents__create_document_from_widget',
            ),
        ),
        Swappable(
            re_path(
                r'^quickforms/image[/]?$',
                quick_forms.QuickImageCreation.as_view(),
                name='documents__create_image_popup',
            ),
        ),
        app_name='documents',
    ).kept_patterns(),
]
