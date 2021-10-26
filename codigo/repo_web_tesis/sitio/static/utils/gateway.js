
const gateway = (content='application/json') => {
    if (!axios) throw new Error("axios lib is required for gateway.");

    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common["Content-Type"] = content;
    axios.defaults.headers.common["X-Requested-With"] = "XMLHttpRequest";

    axios.every = (seconds, action) => {
        return setInterval(action, 1000 * seconds);
    };

    return axios;
};
