<template>
    <div class="content" style="flex-grow: 0">
        <div class="content container">
            <b-notification
                aria-close-label="Close notification"
                v-for="announcement in filteredItems"
                :key="announcement.id"
                v-bind:type="announcement.message_type"
                @close="closeAnnouncement(announcement.id)"
            >
                <vue-markdown> {{ announcement.message }} </vue-markdown>
            </b-notification>
        </div>
    </div>
</template>

<script>
import { mapState } from "vuex";
export default {
    name: "Announcement",
    data() {
        return {};
    },
    methods: {
        closeAnnouncement(announcement) {
            this.$cookie.set("closedAnnouncement" + announcement, true, 14);
        },
        checkRouteName(item) {
            if (!item.route_name || item.route_name == this.$route.name) return true;
            return false;
        },
    },

    computed: {
        ...mapState({
            fetchedAnnouncements: (state) => state.announcements.announcements,
        }),
        filteredItems() {
            return this.fetchedAnnouncements.filter((item) => {
                return (
                    !this.$cookie.get("closedAnnouncement" + item.id) &&
                    this.checkRouteName(item)
                );
            });
        },
    },
    created() {
        this.$store.dispatch("announcements/getAnnouncements");
    },
};
</script>

<style>
.media-content div h1,
.media-content div h2,
.media-content div h3 {
    color: #fff;
}
</style>
