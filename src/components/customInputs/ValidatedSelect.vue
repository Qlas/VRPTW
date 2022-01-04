<template>
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

            <b-taginput v-if="multiple" v-bind="$attrs" v-on="$listeners">
                <template v-if="addNew" slot="footer">
                    <a @click="$emit('addNewClick', true)">
                        <span> Add new... </span>
                    </a>
                </template>
                <template slot="empty">No results found</template>
            </b-taginput>

            <b-autocomplete v-else v-bind="$attrs" v-on="$listeners">
                <template v-if="addNew" slot="footer">
                    <a @click="$emit('addNewClick', true)">
                        <span> Add new... </span>
                    </a>
                </template>
                <template slot="empty">No results found</template>
            </b-autocomplete>
        </b-field>
    </ValidationProvider>
</template>

<script>
export default {
    name: "ValidatedSelect",
    inheritAttrs: false,

    props: {
        field: { type: Object },
        validation: { type: Object },
        multiple: { type: Boolean, default: false },
        addNew: { type: Boolean, default: false },
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
