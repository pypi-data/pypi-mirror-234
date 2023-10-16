window.addEventListener("DOMContentLoaded", () => {

    // Return whether the form fields under the current form-container are empty.
    function isEmpty(form) {
        for (const elem of form.querySelectorAll(".fields-container input:not([type=hidden]),select,textarea")) {
            if ((elem.type === "checkbox" && elem.checked) || elem.value.trim()) return false 
        }
        return true
    }

    // Return the management form element that stores the form count.
    function getTotalFormsElement(formset) {
        return formset.querySelector("[id$=TOTAL_FORMS")
    }

    function updateTotalCount(formset, count) {
        getTotalFormsElement(formset).value = count
    }

    function getTotalCount(formset){
        return parseInt(getTotalFormsElement(formset).value, 10)
    }

    function getFormsetPrefix(formset) {
        return formset.dataset.prefix
    }

    function getFormPrefix(form) {
        return getFormsetPrefix(form.parentNode)
    }

    // Update the prefix indices of the fields belonging to the given form.
    function updatePrefixes(form, index) {
        const prefix = getFormPrefix(form)
        // __prefix__ is the default prefix of empty forms
        const regex = new RegExp(`(${prefix}-(\\d+|__prefix__))`)
        form.querySelectorAll("*").forEach((elem) => {
            for (const attr of ["id", "name", "for"]) {
                if (elem.hasAttribute(attr)) {
                    elem.setAttribute(attr, elem.getAttribute(attr).replace(regex, `${prefix}-${index}`))
                }
            } 
        })
    }

    function disableElem(elem){
        elem.disabled = true
        elem.classList.add("disabled-for-removal")
    }

    function enableElem(elem){
        elem.disabled = false
        elem.classList.remove("disabled-for-removal")
    }

    /* Handle clicking on the delete button of a form. 

    If the form is an extra form without data, remove it from the DOM.
    If the form is not empty, or if it is not an extra form, check the (hidden) 
    DELETE checkbox, disable the form and mark it for removal. Pressing the
    delete button again undoes the changes.
    */
    function deleteHandler(btn) {
        btn.addEventListener("click", (e) => {
            e.preventDefault()
            const form = btn.parentNode.parentNode
            const formset = form.parentNode
            if (form.classList.contains("extra-form") && isEmpty(form)) {
                // Manipulating the number of forms requires updating the 
                // management form and the prefixes.
                form.remove()
                updateTotalCount(formset, getTotalCount(formset) - 1)
                let index = 0
                formset.querySelectorAll(":scope > .form-container").forEach((f) => {
                    if (f.classList.contains("extra-form")) updatePrefixes(f, index)
                    index = index + 1
                })
            }
            else {
                const removing = !form.classList.contains("marked-for-removal")
                form.classList.toggle("marked-for-removal")
                const checkbox = form.querySelector(".delete-cb")
                checkbox.checked = !checkbox.checked
                form.querySelectorAll(".form-control,.form-select").forEach((elem) => {
                    if (removing && !elem.disabled) {
                        // Currently marking the form for removal, and the elem 
                        // was not already disabled (do not mess with already 
                        // disabled controls).
                        disableElem(elem)
                    }
                    else if (!removing && elem.classList.contains("disabled-for-removal")) {
                        // Currently un-marking the form, and the elem was 
                        // previously disabled for removal.
                        enableElem(elem)
                    }
                })
            }
        })
    }

    // Handle clicking the 'add another' button, adding an empty, extra form.
    function addHandler(btn) {
        btn.addEventListener("click", (e) => {
            e.preventDefault()

            const addRow = btn.parentNode
            const formset = addRow.parentNode

            const newForm = addRow.querySelector(".empty-form > div").cloneNode(true)
            formset.insertBefore(newForm, addRow)
            const deleteButton = newForm.querySelector(".inline-delete-btn")
            if (deleteButton) deleteHandler(deleteButton)
            newForm.scrollIntoView()

            // Update management form and set the prefixes of the new form.
            const count = getTotalCount(formset) + 1
            updateTotalCount(formset, count)
            updatePrefixes(newForm, count - 1)
        })
    }

    document.querySelectorAll(".inline-delete-btn").forEach((btn) => deleteHandler(btn))
    document.querySelectorAll(".inline-add-btn").forEach((btn) => addHandler(btn))
    window.addEventListener("reset", (e) => {
        document.querySelectorAll(".marked-for-removal").forEach((form) => form.classList.remove("marked-for-removal"))
        document.querySelectorAll(".disabled-for-removal").forEach((elem) => enableElem(elem))
    })
    const deleteStyle = document.createElement("style")
    // Insert at the very top so that the style can be overwritten.
    document.head.insertBefore(deleteStyle, document.head.firstChild)
    deleteStyle.sheet.insertRule(`.marked-for-removal {
        color: gray;
        background-color: lightgray;
        background-image: repeating-linear-gradient(-45deg, transparent, transparent 4px, rgba(255, 255, 255, 0.5) 4px, rgba(255, 255, 255, 0.5) 8px);
        background-size: contain;
        cursor: not-allowed;
    }`)
})
