
import pytest
import time
import datetime
from os import environ
from os import getenv
from embedops_cli.eotools.ci_run import CIRun
from pytest_httpserver import HTTPServer
from embedops_cli.config import settings


class TestTimeoutsAndRetries:
    @pytest.fixture(scope="session")
    def httpserver_listen_address(self):
        return ("127.0.0.1", 1024)
    @pytest.fixture(autouse=True)
    def configure_env(self, monkeypatch, mocker):
        monkeypatch.setenv("CI", "true")
        monkeypatch.setenv("EMBEDOPS_HOST", "127.0.0.1:1024")
        settings.host = "127.0.0.1:1024"
        monkeypatch.setenv("EMBEDOPS_API_REPO_KEY", "special_pwefix")
        monkeypatch.setenv("EMBEDOPS_ANALYSIS_TYPE", "memusage")
        monkeypatch.setenv("EMBEDOPS_HTTP_TIMEOUT", "1")
        monkeypatch.setenv("EMBEDOPS_MAX_RETRIES", "2")
        monkeypatch.setenv("BITBUCKET_COMMIT", "aaaaaa")
        monkeypatch.setenv("BITBUCKET_BRANCH", "main")
        monkeypatch.setenv(
            "BITBUCKET_GIT_HTTP_ORIGIN", "http://bitbucket.org/dojofive/embedops-tools"
        )
        monkeypatch.setenv("BITBUCKET_BUILD_NUMBER", "1")
        monkeypatch.setenv("BITBUCKET_STEP_UUID", "fee-fie-foe-fum")
        self.logger_mock = mocker.patch("embedops_cli.eotools.ci_run._logger")


    def test_server_always_responds_with_503(self, monkeypatch, mocker, httpserver: HTTPServer):
        """
            verify that when the client receives a 503, it will retry max_retries times
            and eventually exit 1 if the server never comes back up
        """
        for _ in range(0, int(getenv("EMBEDOPS_MAX_RETRIES"))):
            httpserver.expect_request(
                "/api/v1/ci/ci-runs",
                method="POST"
            ).respond_with_data(
                "Service Temporarily Unavailable",
                status=503
            )
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            CIRun().create_main()
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1


    def test_server_responds_with_503_then_comes_back(self, monkeypatch, mocker, httpserver: HTTPServer):
        """
            verify that when the client receives a bunch of 503s but
            then it eventually comes back up that we don't raise any exceptions
        """
        for _ in range(0, int(getenv("EMBEDOPS_MAX_RETRIES")) - 1):
            httpserver.expect_oneshot_request(
                "/api/v1/ci/ci-runs",
                method="POST"
            ).respond_with_data(
                "Service Temporarily Unavailable",
                status=503
            )
        httpserver.expect_request(
            "/api/v1/ci/ci-runs",
            method="POST"
        ).respond_with_json(
            {
                "branch": "foo",
                "commitId": "blah",
                "name": "name",
                "pipelineId": "pipelineId",
                "pipelineUrl": "pipelineUrl",
                "status": "running",
                "type": "memusage",
                "createdAt": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                "updatedAt": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                "id": "happydays",
                "repoId": "flooodeeeblaaaahhh",
            },
            status=200
        )
        assert CIRun().create_main()


    def test_server_times_out_and_maximum_retries(self, monkeypatch, mocker, httpserver: HTTPServer):
        """
            verify exit 1 if all requests time out up to max_retries
        """
        def slow_handler(response):
            # response is never received because the server
            # always takes longer that the client's timeout
            time.sleep(1 + int(getenv("EMBEDOPS_HTTP_TIMEOUT")))
            response.data = "OK"
            response.status = 200
            return response

        for _ in range(0, int(getenv("EMBEDOPS_MAX_RETRIES"))):
            httpserver.expect_oneshot_request(
                "/api/v1/ci/ci-runs",
                method="POST"
            ).respond_with_handler(
                slow_handler
            )

        with pytest.raises(SystemExit) as pytest_wrapped_e:
            CIRun().create_main()
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1

    def test_max_client_wait_time_is_max_retries_plus_one(self, monkeypatch, mocker, httpserver: HTTPServer):
        """
            same as test_server_times_out_and_maximum_retries but also
            verifies that the following formula can determine how long
            the maximum time the client can wait for a create_ci_run
            call according to max retries and http_timeout

            max time >= http_timeout(max_retries + 1)
        """
        def slow_handler(response):
            # response is never received because the server
            # always takes longer that the client's timeout
            time.sleep(1 + int(getenv("EMBEDOPS_HTTP_TIMEOUT")))
            response.data = "OK"
            response.status = 200
            return response

        for _ in range(0, int(getenv("EMBEDOPS_MAX_RETRIES"))):
            httpserver.expect_oneshot_request(
                "/api/v1/ci/ci-runs",
                method="POST"
            ).respond_with_handler(
                slow_handler
            )

        start_time = time.monotonic()
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            CIRun().create_main()
        # validate we still exit 1 if we exceed max retries
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1
        end_time = time.monotonic()
        lapsed_time = end_time - start_time
        assert lapsed_time >= int(getenv("EMBEDOPS_HTTP_TIMEOUT"))*(int(getenv("EMBEDOPS_MAX_RETRIES")) + 1)

    def test_default_behavior_when_options_not_set(self, monkeypatch, mocker, httpserver: HTTPServer):
        """
            verify that when the client receives a bunch of 503s but
            then it eventually comes back up that we don't raise any exceptions
        """
        environ.pop("EMBEDOPS_HTTP_TIMEOUT")
        environ.pop("EMBEDOPS_MAX_RETRIES")
        httpserver.expect_request(
            "/api/v1/ci/ci-runs",
            method="POST"
        ).respond_with_json(
            {
                "branch": "foo",
                "commitId": "blah",
                "name": "name",
                "pipelineId": "pipelineId",
                "pipelineUrl": "pipelineUrl",
                "status": "running",
                "type": "memusage",
                "createdAt": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                "updatedAt": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                "id": "happydays",
                "repoId": "flooodeeeblaaaahhh",
            },
            status=200
        )
        assert CIRun().create_main()


    def test_no_retries_on_successful_create(self, monkeypatch, mocker, httpserver: HTTPServer):
        """
            verify that when the client receives a good response from the server
            that it returns immediately without any further retries
        """
        monkeypatch.setenv("EMBEDOPS_HTTP_TIMEOUT", "10")
        monkeypatch.setenv("EMBEDOPS_MAX_RETRIES", "6")

        httpserver.expect_request(
            "/api/v1/ci/ci-runs",
            method="POST"
        ).respond_with_json(
            {
                "branch": "foo",
                "commitId": "blah",
                "name": "name",
                "pipelineId": "pipelineId",
                "pipelineUrl": "pipelineUrl",
                "status": "running",
                "type": "memusage",
                "createdAt": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                "updatedAt": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                "id": "happydays",
                "repoId": "flooodeeeblaaaahhh",
            },
            status=200
        )
        start_time = time.monotonic()
        run_id = CIRun().create_main()
        assert run_id
        print(f'FOO: {run_id}')
        end_time = time.monotonic()
        lapsed_time = end_time - start_time
        # verify that this should take no more than one http timeout
        assert lapsed_time <= int(getenv("EMBEDOPS_HTTP_TIMEOUT"))


class TestNoSuchHost:
    @pytest.fixture(scope="session")
    def httpserver_listen_address(self):
        return ("127.0.0.1", 1024)
    @pytest.fixture(autouse=True)
    def configure_env(self, monkeypatch, mocker):
        monkeypatch.setenv("CI", "true")
        monkeypatch.setenv("EMBEDOPS_HOST", "badhostname.foo")
        settings.host = "127.0.0.1:1024"
        monkeypatch.setenv("EMBEDOPS_API_REPO_KEY", "special_pwefix")
        monkeypatch.setenv("EMBEDOPS_ANALYSIS_TYPE", "memusage")
        monkeypatch.setenv("EMBEDOPS_HTTP_TIMEOUT", "1")
        monkeypatch.setenv("EMBEDOPS_MAX_RETRIES", "2")
        monkeypatch.setenv("BITBUCKET_COMMIT", "aaaaaa")
        monkeypatch.setenv("BITBUCKET_BRANCH", "main")
        monkeypatch.setenv(
            "BITBUCKET_GIT_HTTP_ORIGIN", "http://bitbucket.org/dojofive/embedops-tools"
        )
        monkeypatch.setenv("BITBUCKET_BUILD_NUMBER", "1")
        monkeypatch.setenv("BITBUCKET_STEP_UUID", "fee-fie-foe-fum")
        self.logger_mock = mocker.patch("embedops_cli.eotools.ci_run._logger")


    def test_no_such_server(self, monkeypatch, mocker, httpserver: HTTPServer):
        """
            validates that create-run will exit 1 after too
            long of calling a server that isn't there
        """
        httpserver.expect_request(
            "/api/v1/ci/ci-runs",
            method="POST"
        ).respond_with_data(
            "Service Temporarily Unavailable",
            status=503
        )
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            CIRun().create_main()
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1
