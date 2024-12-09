// app.js

new Vue({
  el: "#app",
  data: {
    data: [],
    searchQuery: "",
    sortKey: "stars",
    sortDirection: -1,
    selectedTags: [],
    currentPage: 1, // 当前页码
    itemsPerPage: 10, // 每页显示的项目数
  },
  computed: {
    sortedData() {
      return this.data
        .slice()
        .sort((a, b) => this.sortDirection * (a[this.sortKey] - b[this.sortKey]));
    },
    filteredData() {
      return this.sortedData.filter((repository) => {
        const location =
          repository.url.split("/")[3] +
          "/" +
          repository.url.split("/")[4].split(".")[0];
        const description = repository.description || "";
        const tags = repository.path
          .replace("projects/", "")
          .split("/")
          .slice(0, -1);

        const tagFilter = this.selectedTags.every((tag) => tags.includes(tag));

        return (
          tagFilter &&
          (description.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
            location.toLowerCase().includes(this.searchQuery.toLowerCase()))
        );
      });
    },
    paginatedData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredData.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredData.length / this.itemsPerPage);
    },
  },
  async created() {
    const response = await fetch(
      "https://raw.githubusercontent.com/adminlove520/securitytools/main/docs/directory.json"
    );
    this.data = await response.json();
  },
  methods: {
    sortBy(key) {
      this.sortDirection = this.sortKey === key ? -this.sortDirection : -1;
      this.sortKey = key;
    },
    toggleTag(tag) {
      const index = this.selectedTags.indexOf(tag);
      if (index >= 0) {
        this.selectedTags.splice(index, 1);
      } else {
        this.selectedTags.push(tag);
      }
    },
    generateTagColor(tag) {
      let hash = 0;
      for (let i = 0; i < tag.length; i++) {
        hash = tag.charCodeAt(i) + ((hash << 5) - hash);
      }

      const c = (hash & 0x00ffffff).toString(16).toUpperCase();
      const color = "00000".substring(0, 6 - c.length) + c;

      return "#" + color;
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    goToPage(page) {
      this.currentPage = page;
    },
  },
});