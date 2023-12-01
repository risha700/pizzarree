import Form from "./Form";
class MultipartForm extends Form {
  /**
   * Override data method to match multipart signature.
   */
  data() {
    let formData = new FormData();

    for (let property in this.originalData) {
      this.prepare_nested_form_data(formData, property);
    }

    return formData;
  }

  /**
   * Assign fields to formData object
   * */
  prepare_nested_form_data(formData, property) {
    if (typeof this.originalData[property] === "object") {
      Object.entries(this.originalData[property]).forEach(([key, value]) =>
        formData.append(`${property}.${key}`, value)
      );
    } else {
      formData.append(property, this[property]);
    }
  }
  /**
   * Reset the form fields.
   */
  reset() {
    for (let field in this.originalData) {
      if (typeof this[field] === "string") {
        this[field] = "";
      } else {
        Object.keys(this[field]).forEach((key) => (this[field][key] = ""));
      }
    }
    this.errors.clear();
  }
}

export default MultipartForm;
