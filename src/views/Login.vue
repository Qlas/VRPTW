<template>
    <form class="login" @submit.prevent="login">
        <div class="columns is-center">
            <div class="column is-two-fifths box">
                <b-field
                    label="Username"
                    :type="wrongCredentialsProvided ? 'is-danger' : ''"
                    :message="
                        wrongCredentialsProvided
                            ? 'The email or password is incorrect.'
                            : ''
                    "
                >
                    <b-input
                        required
                        v-model="username"
                        placeholder="e.g. jkowalski"
                        icon="account"
                        data-cy="username"
                    ></b-input>
                </b-field>

                <b-field label="Password">
                    <b-input
                        required
                        v-model="password"
                        type="password"
                        password-reveal
                        icon="lock"
                        data-cy="password"
                    ></b-input>
                </b-field>

                <div class="buttons is-right">
                    <b-button type="is-primary" native-type="submit" data-cy="button"
                        >Login</b-button
                    >
                </div>
            </div>
        </div>
    </form>
</template>

<script>
import { mapActions } from "vuex";

export default {
    name: "Login",
    data() {
        return {
            wrongCredentialsProvided: false,
            username: "",
            password: "",
        };
    },
    methods: {
        ...mapActions("auth", ["getTokenPair"]),

        login() {
            this.getTokenPair({
                username: this.username,
                password: this.password,
            })
                .then(() => {
                    this.$router.push("/");
                    this.$buefy.notification.open({
                        duration: 8000,
                        message: `Successfull login!`,
                        position: "is-top-right",
                        type: "is-success",
                        hasIcon: true,
                    });
                })
                .catch((err) => {
                    if (err.response.status == 401) {
                        this.password = "";
                        this.wrongCredentialsProvided = true;
                    } else {
                        this.$buefy.notification.open({
                            duration: 8000,
                            message: `Request failed with status <b>${err.response.status}</b>. Please try again in a moment. Otherwise contact administrator.`,
                            position: "is-top-right",
                            type: "is-danger",
                            hasIcon: true,
                        });
                    }
                });
        },
    },
};
</script>

<style scoped>
.is-center {
    height: 75vh;
    display: flex;
    flex-wrap: nowrap;
    justify-content: center;
    align-items: center;
}
</style>
