import tempfile
import unittest
from unittest.mock import MagicMock, Mock, patch
from unittest import TestCase
from selenium.webdriver.common.by import By
from src.google_books_driver.retrieve import (
    extract_report_content,
    get_report,
    build_report_url,
    login_google,
    fetch_report
)


class TestRetrieve(TestCase):
    def setUp(self) -> None:
        return

    def tearDown(self) -> None:
        # Clean up temporary files after each test
        tempfile.tempdir = None

    def test_login_google(self) -> None:
        """Test the log_in is successful first with the user
        then with the password."""
        # Mock the webdriver and its methods
        mock_driver = Mock()
        mock_driver.find_element.return_value = Mock()
        mock_driver.find_element.return_value.send_keys.return_value = None
        mock_driver.find_element.return_value.click.return_value = None
        mock_driver.get.return_value = None

        # Patch the webdriver.Chrome class with the mock driver
        mock_chrome = Mock()
        mock_chrome.return_value = mock_driver
        patcher = unittest.mock.patch(
            "src.google_books_driver.retrieve.webdriver.Chrome",
            mock_chrome
        )
        patcher.start()

        # Call the method under test
        user = "test_user"
        password = "test_password"
        driver = login_google(mock_driver, identifier=user)
        # Assert that the webdriver methods were called correctly
        mock_driver.get.assert_called_with(
            "https://accounts.google.com/ServiceLogin"
        )
        mock_driver.find_element.assert_called_with(By.ID, "identifierNext")
        mock_driver.find_element.return_value.send_keys.assert_called_with(user)
        self.assertEqual(mock_driver.find_element.call_count, 2)

        driver = login_google(mock_driver, Passwd=password)
        mock_driver.find_element.assert_called_with(By.ID, "passwordNext")
        mock_driver.find_element.return_value.send_keys.assert_called_with(
            password
        )
        self.assertEqual(mock_driver.find_element.call_count, 4)

        # Assert that the driver instance is returned
        self.assertTrue(driver is not None)

    def test_build_report_url_and_params_successful(self) -> None:
        url, params = build_report_url(
            "test_gb_account", start_date="1999-02-04", end_date="1999-02-12"
        )
        self.assertEqual(
            url,
            (
                "https://play.google.com/books/publish/u/0/a/test_gb_account/"
                "downloadTrafficReport"
            ),
        )
        self.assertEqual(
            params,
            {"f.req": "[[null,1999,2,4],[null,1999,2,12],2,0]"}
        )

    def test_build_report_url_fails(self) -> None:
        with self.assertRaises(ValueError):
            build_report_url(
                "test_gb_account",
                start_date="02-04-1999",
                end_date="02-12-1999"
            )

    @patch("src.google_books_driver.retrieve.requests.get")
    def test_get_report(self, mock_get) -> None:
        # Mock the response
        expected_content = (
            b"\xff\xfeS\x00H\x00A\x00D\x00E\x00K\x00 \x00D\x00E\x00E\x00E\x00P\x00"
        )
        mock_response = MagicMock()
        mock_driver = MagicMock()
        mock_response.status_code = 200
        mock_response.content = expected_content
        mock_response.headers = {
            "content-type": "text/plain",
        }
        mock_get.return_value = mock_response

        # Call the function with test data
        report_url = "https://example.com/report"
        params = {"f.req": "[[null,2023,8,1],[null,2023,8,10],2,0]"}
        cookies = {
            cookie["name"]: cookie["value"]
            for cookie in mock_driver.get_cookies()
            if cookie["domain"] == ".google.com"
        }
        result = get_report(report_url, mock_driver, params)

        # Assertions
        mock_get.assert_called_once_with(
            report_url, cookies=cookies, params=params
        )
        self.assertEqual(result, "SHADEK DEEEP")

    @patch("src.google_books_driver.retrieve.requests.get")
    def test_get_report_bad_reponse(self, mock_get) -> None:
        # Mock the response
        expected_content = (
            b"\xff\xfeS\x00H\x00A\x00D\x00E\x00K\x00 \x00D\x00E\x00E\x00E\x00P\x00"
        )
        mock_response = MagicMock()
        mock_driver = MagicMock()
        mock_response.status_code = 400
        mock_response.content = expected_content
        mock_response.headers = {
            "content-type": "text/plain",
        }
        mock_get.return_value = mock_response

        # Call the function with test data
        report_url = "https://example.com/report"
        params = {"f.req": "[[null,2023,8,1],[null,2023,8,10],2,0]"}
        with self.assertRaises(OSError):
            get_report(report_url, mock_driver, params)

    def test_extract_report_content(self) -> None:
        """Make sure the spaces are tab-separated for each cell and there is
        a new line at the end (THE SHELL WON'T PRINT IT FOR YOU)."""
        report_content = (
            '"Primary ISBN"\t"Title"\t"Book Visits (BV)"\t"BV with Pages'
            ' Viewed"\t"Non-Unique Buy Clicks"\t"BV with Buy Clicks"\t"'
            'Buy Link CTR"\t"Pages Viewed"\n"1234567890123"\t"Conversations'
            ' with Test"\t"1"\t"1"\t"0"\t"0"\t"0.0%"\t"1"\n"1234567890123"'
            '\t"Strindberg and AutobTest"\t"6"\t"6"\t"0"\t"0"\t'
            '"0.0%"\t"9"\n"4567890123456"\t"Studies in Test"\t"6"\t"6"'
            '\t"0"\t"0"\t"0.0%"\t"7"\n"9781909188174"\t"Testnte and Testinas'
            '"\t"7"\t"7"\t"0"\t"0"\t"0.0%"\t"7"\n'
        )
        expected_headers = [
            "Primary ISBN",
            "Title",
            "Book Visits (BV)",
            "BV with Pages Viewed",
            "Non-Unique Buy Clicks",
            "BV with Buy Clicks",
            "Buy Link CTR",
            "Pages Viewed"
        ]
        expected_result = [
            {
                "Primary ISBN": "1234567890123",
                "Title": "Conversations with Test",
                "Book Visits (BV)": "1",
                "BV with Pages Viewed": "1",
                "Non-Unique Buy Clicks": "0",
                "BV with Buy Clicks": "0",
                "Buy Link CTR": "0.0%",
                "Pages Viewed": "1",
            },
            {
                "Primary ISBN": "1234567890123",
                "Title": "Strindberg and AutobTest",
                "Book Visits (BV)": "6",
                "BV with Pages Viewed": "6",
                "Non-Unique Buy Clicks": "0",
                "BV with Buy Clicks": "0",
                "Buy Link CTR": "0.0%",
                "Pages Viewed": "9",
            },
            {
                "Primary ISBN": "4567890123456",
                "Title": "Studies in Test",
                "Book Visits (BV)": "6",
                "BV with Pages Viewed": "6",
                "Non-Unique Buy Clicks": "0",
                "BV with Buy Clicks": "0",
                "Buy Link CTR": "0.0%",
                "Pages Viewed": "7",
            },
            {
                "Primary ISBN": "9781909188174",
                "Title": "Testnte and Testinas",
                "Book Visits (BV)": "7",
                "BV with Pages Viewed": "7",
                "Non-Unique Buy Clicks": "0",
                "BV with Buy Clicks": "0",
                "Buy Link CTR": "0.0%",
                "Pages Viewed": "7",
            },
        ]
        self.assertEqual(
            extract_report_content(report_content, expected_headers),
            expected_result
        )

    def test_extract_report_content_wrong_headers(self) -> None:
        headers = ["WRONG ISBN", "WRONG Title", "Book Visits (BV)"]
        result = (
            '"Primary ISBN"\t"Title"\t"Book Visits (BV)"\t"BV with Pages'
            ' Viewed"\t"Non-Unique Buy Clicks"\t"BV with Buy Clicks"\t"'
            'Buy Link CTR"\t"Pages Viewed"\n"1234567890123"\t"Conversations'
            ' with Test"\t"1"\t"1"\t"0"\t"0"\t"0.0%"\t"1"\n"1234567890123"'
            '\t"Strindberg and AutobTest"\t"6"\t"6"\t"0"\t"0"\t'
            '"0.0%"\t"9"\n"4567890123456"\t"Studies in Test"\t"6"\t"6"'
            '\t"0"\t"0"\t"0.0%"\t"7"\n"9781909188174"\t"Testnte and Testinas'
            '"\t"7"\t"7"\t"0"\t"0"\t"0.0%"\t"7"\n'
        )
        with self.assertRaises(ValueError):
            extract_report_content(result, expected_headers=headers)

    def test_extract_report_content_with_csv_file(self) -> None:
        """Test the extract_report_content method using a tempfile."""
        csv_data = "\t".join(
            ["Primary ISBN", "Title", "Book Visits (BV)"]
        ) + "\n"
        csv_data += "\t".join(
            ["4567890123456", "Studies in Test", "1"]
        ) + "\n"
        csv_data += "\t".join(
            ["9781909188174", "Testnte and Testinas", "2"]
        ) + "\n"

        with tempfile.NamedTemporaryFile(
            mode="w+", delete=False, encoding="utf-16"
        ) as temp_file:
            temp_file.write(csv_data)

        expected_result = [
            {
                "Primary ISBN": "4567890123456",
                "Title": "Studies in Test",
                "Book Visits (BV)": "1",
            },
            {
                "Primary ISBN": "9781909188174",
                "Title": "Testnte and Testinas",
                "Book Visits (BV)": "2",
            }
        ]
        with open(temp_file.name, "r", encoding="utf-16") as f:
            results = f.read()
        result = extract_report_content(
            report_content=results,
            expected_headers=["Primary ISBN", "Title", "Book Visits (BV)"]
        )
        self.assertEqual(result, expected_result)

    @patch("src.google_books_driver.retrieve.webdriver.Chrome")
    @patch("src.google_books_driver.retrieve.initialize_service")
    @patch("src.google_books_driver.retrieve.get_report")
    def test_fetch_report_with_credentials(
            self, mock_logger, mock_initialize_service, mock_get_report
    ) -> None:
        """Test the resturn_results method using creds for selenium."""
        mock_result = (
            '"Primary ISBN"\t"Title"\t"Book Visits (BV)"\t"BV with Pages'
            ' Viewed"\t"Non-Unique Buy Clicks"\t"BV with Buy Clicks"\t"'
            'Buy Link CTR"\t"Pages Viewed"\n"1234567890123"\t"Conversations'
            ' with Test"\t"1"\t"1"\t"0"\t"0"\t"0.0%"\t"1"\n"1234567890123"'
            '\t"Strindberg and AutobTest"\t"6"\t"6"\t"0"\t"0"\t'
            '"0.0%"\t"9"\n"4567890123456"\t"Studies in Test"\t"6"\t"6"'
            '\t"0"\t"0"\t"0.0%"\t"7"\n"9781909188174"\t"Testnte and Testinas'
            '"\t"7"\t"7"\t"0"\t"0"\t"0.0%"\t"7"\n'
        )
        # Configure mock responses
        mock_service = Mock()
        mock_service.close.return_value = None
        mock_initialize_service.return_value = mock_service
        mock_get_report.return_value = mock_result

        credentials = {
                "gb_account": 12345,
                "user": "test_user",
                "password": "test_passw",
                "start_date": "2023-01-08",
                "end_date": "2023-10-08",
                "path_to_driver": "/usr/local/test_dir"
        }
        # The return would be <MagicMock name='get_report()' id='random_id'>
        self.assertNotEqual(fetch_report(**credentials), None)
