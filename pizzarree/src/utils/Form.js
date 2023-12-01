import FormErrors from "./FormErrors";
import { api } from "src/boot/axios";

class Form {
  /**
   * Create a new Form instance.
   *
   * @param {object} data
   */
  constructor(data) {
    this.originalData = data;

    for (let field in data) {
      this[field] = data[field];
    }

    this.errors = new FormErrors();
  }

  /**
   * Fetch all relevant data for the form.
   */
  data() {
    let data = {};

    for (let property in this.originalData) {
      data[property] = this[property];
    }

    return data;
  }

  /**
   * Reset the form fields.
   */
  reset() {
    for (let field in this.originalData) {
      this[field] = "";
    }
    this.errors.clear();
  }

  /**
   * Send a POST request to the given URL.
   * .
   * @param {string} url
   */
  post(url) {
    return this.submit("post", url);
  }

  /**
   * Send a PUT request to the given URL.
   * .
   * @param {string} url
   */
  put(url) {
    return this.submit("put", url);
  }

  /**
   * Send a PATCH request to the given URL.
   * .
   * @param {string} url
   */
  patch(url) {
    return this.submit("patch", url);
  }

  /**
   * Send a DELETE request to the given URL.
   * .
   * @param {string} url
   */
  delete(url) {
    return this.submit("delete", url);
  }

  /**
   * Submit the form.
   *
   * @param {string} requestType
   * @param {string} url
   */
  submit(requestType, url) {
    this.errors.clear();
    return new Promise((resolve, reject) => {
      api[requestType](url, this.data())
        .then((response) => {
          this.onSuccess();
          resolve(response.data);
          this.onFinished();
        })
        .catch((error) => {
          // model errors
          if (error.response) {
            this.onFail(error.response.data);
            reject(error.response.data);
          } else {
            // server errors
            this.onFail(error.message);
            reject(error.message);
          }
          this.onFinished();
        });
    });
  }

  /**
   * Handle a successful form submission.
   *
   * @param {object} data
   */
  onSuccess() {
    this.reset();
  }

  /**
   * Handle a failed form submission.
   *
   * @param {object} errors
   */
  onFail(errors) {
    this.errors.record(errors);
  }
  /**
   * Handle a successful or rejected form submission.
   *
   * @param {object} data
   */
  onFinished() {
    // this.reset();
  }

  /**
   * Determine if the error is non_field_error then show a banner
   */
  commonErrors() {
    let common_err = true;
    for (let field in this.originalData) {
      if (this.errors.has(field)) common_err = false;
    }
    return this.errors.any() && common_err;
  }
}

export default Form;
