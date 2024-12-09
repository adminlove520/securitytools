new Vue({
  el: '#app',
  data: {
    repos: [],
    searchQuery: '',
    selectedTags: [],
    currentPage: 1,
    itemsPerPage: 10 // Number of items per page
  },
  computed: {
    totalPages() {
      return Math.ceil(this.filteredData.length / this.itemsPerPage);
    },
    filteredData() {
      let filtered = this.repos;
      if (this.searchQuery) {
        filtered = filtered.filter(repo =>
          repo.description.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          repo.url.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }
      if (this.selectedTags.length > 0) {
        filtered = filtered.filter(repo =>
          this.selectedTags.every(tag => repo.path.includes(tag))
        );
      }
      return filtered;
    },
    paginatedData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredData.slice(start, end);
    }
  },
  methods: {
    sortBy(column) {
      this.repos.sort((a, b) => {
        if (column === 'location') {
          return a.path.localeCompare(b.path);
        } else if (column === 'description') {
          return a.description.localeCompare(b.description);
        } else if (column === 'watchers') {
          return b.watchers - a.watchers;
        } else if (column === 'forks') {
          return b.forks - a.forks;
        } else if (column === 'stars') {
          return b.stars - a.stars;
        }
        return 0;
      });
    },
    toggleTag(tag) {
      if (this.selectedTags.includes(tag)) {
        this.selectedTags = this.selectedTags.filter(t => t !== tag);
      } else {
        this.selectedTags.push(tag);
      }
    },
    generateTagColor(tag) {
      // Simple hash function to generate a color based on the tag
      let hash = 0;
      for (let i = 0; i < tag.length; i++) {
        hash = tag.charCodeAt(i) + ((hash << 5) - hash);
      }
      const c = (hash & 0x00FFFFFF).toString(16).toUpperCase();
      return '#' + '00000'.substring(0, 6 - c.length) + c;
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
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    }
  },
  mounted() {
    fetch('https://api.github.com/users/adminlove520/repos')
      .then(response => response.json())
      .then(data => {
        this.repos = data.map(repo => ({
          path: repo.full_name.replace('adminlove520/', ''),
          url: repo.html_url,
          description: repo.description || 'No description available',
          watchers: repo.watchers_count,
          forks: repo.forks_count,
          stars: repo.stargazers_count
        }));
      })
      .catch(error => console.error('Error fetching repositories:', error));
  }
});