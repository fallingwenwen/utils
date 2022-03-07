class generateStructure {
    constructor(options) {
        this.structure = {
            "widgetList": [],
            "formConfig": this.getFormConfig()
        }
        for (let index = 0; index < options.length; index++) {
            const el = options[index];
            let row = this.getRow(el);
            this.structure.widgetList.push(row);
        }
        console.log(JSON.stringify(this.structure))

    }
    getRow(el) {
        let row;
        switch (el.type) {
            case "number":
                row = this.getNumber(el);
                break;
            case "input":
                row = this.getInput(el);
                break;
            case "date":
                row = this.getDate(el);
                break;

            default:
                break;
        }
        return row;
    }
    getNumber(option) {
        let id = this.randomNum(5, option["type"]);
        return {
            "type": "number",
            "icon": "number-field",
            "formItemFlag": true,
            "options": {
                "name": option["name"],
                "label": option["name"],
                "labelAlign": "",
                "defaultValue": 0,
                "placeholder": "",
                "columnWidth": "200px",
                "size": "",
                "labelWidth": null,
                "labelHidden": false,
                "disabled": false,
                "hidden": false,
                "required": false,
                "validation": "",
                "validationHint": "",
                "customClass": "",
                "labelIconClass": null,
                "labelIconPosition": "rear",
                "labelTooltip": null,
                "min": -100000000000,
                "max": 100000000000,
                "precision": option["len"],
                "step": 1,
                "controlsPosition": "right",
                "onCreated": "",
                "onMounted": "",
                "onChange": "",
                "onFocus": "",
                "onBlur": "",
                "onValidate": ""
            },
            "id": option["name"]
        }
    }
    getInput(option) {
        let id = this.randomNum(5, option["type"]);
        return {
            "type": "input",
            "icon": "text-field",
            "formItemFlag": true,
            "options": {
                "name": option["name"],
                "label": option["name"],
                "labelAlign": "",
                "type": "text",
                "defaultValue": "",
                "placeholder": "",
                "columnWidth": "200px",
                "size": "",
                "labelWidth": null,
                "labelHidden": false,
                "readonly": false,
                "disabled": false,
                "hidden": false,
                "clearable": true,
                "showPassword": false,
                "required": false,
                "validation": "",
                "validationHint": "",
                "customClass": [],
                "labelIconClass": null,
                "labelIconPosition": "rear",
                "labelTooltip": null,
                "minLength": null,
                "maxLength": null,
                "showWordLimit": false,
                "prefixIcon": "",
                "suffixIcon": "",
                "appendButton": false,
                "appendButtonDisabled": false,
                "buttonIcon": "el-icon-search",
                "onCreated": "",
                "onMounted": "",
                "onInput": "",
                "onChange": "",
                "onFocus": "",
                "onBlur": "",
                "onValidate": ""
            },
            "id": option["name"]
        }
    }
    getDate(option) {
        let id = this.randomNum(5, option["type"]);
        return {
            "type": "date",
            "icon": "date-field",
            "formItemFlag": true,
            "options": {
                "name": option["name"],
                "label": option["name"],
                "labelAlign": "",
                "type": "date",
                "defaultValue": null,
                "placeholder": "",
                "columnWidth": "200px",
                "size": "",
                "labelWidth": null,
                "labelHidden": false,
                "readonly": false,
                "disabled": false,
                "hidden": false,
                "clearable": true,
                "editable": false,
                "format": "yyyy-MM-dd HH:mm:ss",
                "valueFormat": "yyyy-MM-dd HH:mm:ss",
                "required": false,
                "validation": "",
                "validationHint": "",
                "customClass": "",
                "labelIconClass": null,
                "labelIconPosition": "rear",
                "labelTooltip": null,
                "onCreated": "",
                "onMounted": "",
                "onChange": "",
                "onFocus": "",
                "onBlur": "",
                "onValidate": ""
            },
            "id": option["name"]
        }
    }
    getFormConfig() {
        return {
            "modelName": "formData",
            "refName": "vForm",
            "rulesName": "rules",
            "labelWidth": 80,
            "labelPosition": "left",
            "size": "",
            "labelAlign": "label-left-align",
            "cssCode": "",
            "customClass": "",
            "functions": "",
            "layoutType": "PC",
            "onFormCreated": "",
            "onFormMounted": "",
            "onFormDataChange": ""
        }
    }
    randomNum(len, type) {
        let radix = 10;
        var chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'.split('');
        var uuid = [],
            i;
        if (len) {
            for (i = 0; i < len; i++) uuid[i] = chars[0 | Math.random() * radix];
        } else {
            var r;
            uuid[8] = uuid[13] = uuid[18] = uuid[23] = '-';
            uuid[14] = '4';
            for (i = 0; i < 36; i++) {
                if (!uuid[i]) {
                    r = 0 | Math.random() * 16;
                    uuid[i] = chars[(i == 19) ? (r & 0x3) | 0x8 : r];
                }
            }
        }
        return type + uuid.join('');
    }
}

new generateStructure([
    { name: "project_code", type: "input" },
    { name: "crane_id", type: "input" },
    { name: "date", type: "date" },
    { name: "work_hour", type: "number", len: 1 },
    { name: "safety_level", type: "number", len: 1 },
    { name: "tower_safety_level", type: "number", len: 1 },
    { name: "operate_safety_level", type: "number", len: 1 },
    { name: "staff_level", type: "number", len: 1 },
    { name: "unauthorized_level", type: "number", len: 1 },
    { name: "violation_level", type: "number", len: 0 }
])