import os, subprocess, shutil, glob

ch3 = {'Chapter3ViewTests.test_index_contains_hello_message': False,
        'Chapter3ViewTests.test_about_contains_create_message': False}

ch4 = {'Chapter4ViewTest.test_view_has_title': False,
        'Chapter4ViewTest.test_index_using_template': False,
        'Chapter4ViewTest.test_about_using_template': False,
        'Chapter4ViewTest.test_rango_picture_displayed': False,
        'Chapter4ViewTest.test_cat_picture_displayed': False,
        'Chapter4ViewTest.test_about_contain_image': False,
        'Chapter4ViewTest.test_serving_static_files': False}

ch5 = {'Chapter5ModelTests.test_create_a_new_category': False,
        'Chapter5ModelTests.test_create_pages_for_categories': False,
        'Chapter5ModelTests.test_population_script_changes': False}

ch6 = {'Chapter6ModelTests.test_category_contains_slug_field': False,
        'Chapter6ViewTests.test_index_context': False,
        'Chapter6ViewTests.test_index_displays_five_most_liked_categories': False,
        'Chapter6ViewTests.test_index_displays_no_categories_message': False,
        'Chapter6ViewTests.test_index_displays_five_most_viewed_pages': False,
        'Chapter6ViewTests.test_index_contains_link_to_categories': False,
        'Chapter6ViewTests.test_category_context': False,
        'Chapter6ViewTests.test_category_page_using_template': False,
        'Chapter6ViewTests.test_category_page_displays_pages': False,
        'Chapter6ViewTests.test_category_page_displays_empty_message': False,
        'Chapter6ViewTests.test_category_page_displays_category_does_not_exist_message': False}

ch7 = {'Chapter7ViewTests.test_index_contains_link_to_add_category': False,
        'Chapter7ViewTests.test_add_category_form_is_displayed_correctly': False,
        'Chapter7ViewTests.test_add_page_form_is_displayed_correctly': False,
        'Chapter7ViewTests.test_access_category_that_does_not_exists': False,
        'Chapter7ViewTests.test_link_to_add_page_only_appears_in_valid_categories': False,
        'Chapter7ViewTests.test_category_contains_link_to_add_page': False}

ch8 = {'Chapter8ViewTests.test_base_template_exists': False,
        'Chapter8ViewTests.test_titles_displayed': False,
        'Chapter8ViewTests.test_pages_using_templates': False,
        'Chapter8ViewTests.test_url_reference_in_index_page_when_logged': False,
        'Chapter8ViewTests.test_url_reference_in_index_page_when_not_logged': False,
        'Chapter8ViewTests.test_link_to_index_in_base_template': False,
        'Chapter8ViewTests.test_url_reference_in_category_page': False}

ch9 = {'Chapter9ModelTests.test_user_profile_model': False,
        'Chapter9ViewTests.test_registration_form_is_displayed_correctly': False,
        'Chapter9ViewTests.test_login_form_is_displayed_correctly': False,
        'Chapter9ViewTests.test_login_provides_error_message': False,
        'Chapter9ViewTests.test_login_redirects_to_index': False,
        'Chapter9ViewTests.test_upload_image': False}

ch10 = {'Chapter10SessionTests.test_user_number_of_access_and_last_access_to_index': False,
        'Chapter10ViewTests.test_index_shows_number_of_visits': False,
        'Chapter10ViewTests.test_about_page_shows_number_of_visits': False,
        'Chapter10ViewTests.test_visit_number_is_passed_via_context': False}

dict_chs = {'chapter3': ch3, 'chapter4': ch4, 'chapter5': ch5, 'chapter6': ch6,
            'chapter7': ch7, 'chapter8': ch8, 'chapter9': ch9, 'chapter10': ch10}

# dict_chs = {'chapter5': ch5}
