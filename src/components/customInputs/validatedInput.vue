<template>
    <div>
        <ValidationProvider
            :name="validation.name"
            :rules="validation.rules"
            v-slot="{ errors }"
        >
            <b-field
                :label-for="field.labelFor"
                :custom-class="field.customClass"
                :grouped="field.grouped"
                :group-multiline="field.groupMultiline"
                :position="field.position"
                :addons="field.addons"
                :horizontal="field.horizontal"
                :label-position="field.labelPosition"
                :type="{ 'is-danger': errors[0] }"
                :message="errors"
            >
                <template #label>
                    {{ field.label
                    }}<span v-if="isRequired" class="has-text-danger">*</span>
                    <b-tooltip
                        v-if="field.helpMsg"
                        type="is-dark"
                        position="is-right"
                        multilined
                        :label="field.helpMsg"
                    >
                        <b-icon size="is-small" icon="help-circle-outline"></b-icon>
                    </b-tooltip>
                </template>
                <b-numberinput
                    v-if="inputType === 'b-numberinput'"
                    v-bind="$attrs"
                    v-on="$listeners"
                />
                <b-input v-else v-bind="$attrs" v-on="$listeners" />
                <p v-if="staticData" class="control">
                    <span class="button is-static">
                        {{ staticData }}
                    </span>
                </p>
            </b-field>
        </ValidationProvider>
    </div>
</template>

<script>
export default {
    name: "ValidatedInput",
    inheritAttrs: false,

    props: {
        inputType: { type: String },
        field: { type: Object },
        validation: { type: Object },
        staticData: { type: String },
    },

    data() {
        return {
            isRequired: false,
        };
    },

    created() {
        let rules = this.validation.rules;
        if (typeof rules === "object") rules = JSON.stringify(rules);
        this.isRequired = rules.includes("required");
    },
};
</script>
