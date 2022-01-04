<template>
    <div class="insufficient-permissions container">
        <h2>Insufficient permissions</h2>
        <img
            class="policeman"
            src="@/assets/insufficient-permissions.png"
            alt="Go to jail"
        />

        <br />

        <b-button
            size="is-large"
            type="is-primary"
            icon-left="arrow-left"
            @click="$router.push('/')"
        >
            <!-- Going back only 1 record does nothing. -->
            Go back
        </b-button>
    </div>
</template>

<script>
export default {
    name: "InsufficientPermissions",
};
</script>

<style>
.insufficient-permissions {
    font-size: 3rem;
    text-align: center;
}

.policeman {
    transform: scaleX(-1);
    margin-right: 8rem;
    width: auto;
}
</style>
