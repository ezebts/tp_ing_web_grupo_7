
class ConnectedComponent extends React.Component {
    constructor(props) {
        super(props);

        this.gateway = gateway();

        this.fetchId = null;
        this.dataSourceURL = props.getUrl || null;
        this.dataStoreURL = props.postUrl || null;

        if (props.url) {
            this.dataSourceURL = props.url;
            this.dataStoreURL = props.url;
        }

        this.fetchData = this.fetchData.bind(this);
        this.connectedParent = props.connectedParent;

        this.fetchFreq = props.fetchFreq || 6;
    }

    componentDidMount() {
        this.fetchData(true);

        if (this.connectedParent) {
            this.connectedParent.fetchData();
        }

        this.fetchId = this.gateway.every(this.fetchFreq, this.fetchData);
    }

    componentWillUnmount() {
        if (this.fetchId) {
            clearInterval(this.fetchId);
        }
    }

    parseJsonResponse(json) {
        return json;
    }

    updateState(prev, parsed) {
        return parsed;
    }

    mustUpdateState(prev, parsed) {
        return prev != parsed;
    }

    fetchData(isInitialFetch = false) {
        if (this.dataSourceURL) {
            this.gateway
                .get(this.dataSourceURL)
                .then((response) => {
                    const redirected = this.getRedirectionURL(response);

                    if (redirected) {
                        window.location.replace(redirected);
                        return;
                    }

                    let data = response.data || null;
                    let contentType = response.headers["content-type"];
                    let isJson = contentType && contentType.indexOf("application/json") !== -1;

                    let parsed = null;

                    if (data && isJson) {
                        parsed = this.parseJsonResponse(data);
                    }

                    if (parsed) {
                        if (this.mustUpdateState(this.state || {}, parsed)) {
                            this.setState((prev) => this.updateState(prev || {}, parsed));
                        }
                    }
                });
        }
    }

    getRedirectionURL(response) {
        const url = response.request.responseURL;
        const apiRedirect = url.indexOf('?next=/api/');
        let destinationURL = response.request.responseURL;

        if (apiRedirect >= 0) {
            destinationURL = url.substring(0, apiRedirect);
            destinationURL += `?next=${window.location.href.replace(window.location.origin, '')}`
        }

        const redirected = destinationURL.indexOf(response.config.url) < 0;

        if (redirected) {
            return destinationURL;
        }

        return null;
    }

    focusNewData() { }

    sendJsonRequest(json) {
        this.gateway
            .post(this.dataStoreURL, json)
            .then((response) => {
                const redirected = this.getRedirectionURL(response);

                if (redirected) {
                    window.location.replace(redirected);
                    return;
                }

                this.fetchData();

                if (this.connectedParent) {
                    this.connectedParent.fetchData();
                    this.connectedParent.focusNewData();
                }
            });
    }
}
