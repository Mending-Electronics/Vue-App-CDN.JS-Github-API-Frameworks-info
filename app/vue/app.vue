const { createApp } = Vue;

    createApp({
        data() {
            return {
                libraries: [],
                releases: {}
            };
        },
        mounted() {
            const libraries = ['jquery', 'bootstrap', 'bootstrap-icons', 'axios', 'vue', 'vuex', 'vue-router'];

            libraries.forEach(library => {
                axios.get(`https://api.cdnjs.com/libraries/${library}`)
                    .then(response => {
                        this.libraries.push(response.data);
                        const repoUrl = response.data.repository.url;
                        const repoApi = repoUrl.replace("github.com/", "api.github.com/repos/");
                        this.fetchReleases(repoApi, library);
                    })
                    .catch(error => console.error('Error fetching data:', error));
            });
        },
        methods: { 

            fetchReleases(repoApi, library) {
                axios.get(`${repoApi}/releases`)
                    .then(response => {
                        this.releases[library] = response.data.slice(0, 10).map(release => ({
                            name: release.name,
                            published_at: release.published_at
                        }));
                    })
                    .catch(error => console.error('Error fetching releases:', error));
            },

            copyToClipboard(text) { 

                const textarea = document.createElement('textarea'); 

                textarea.value = text; 

                document.body.appendChild(textarea); 

                textarea.select(); 

                document.execCommand('copy'); 

                document.body.removeChild(textarea); 

                alert('Copied to clipboard'); 

            }, 

            async copyScriptTag(libraryName, version, file) { 

                const url = `https://cdnjs.cloudflare.com/ajax/libs/${libraryName}/${version}/${file}`; 

                const sriHash = await this.getSriHash(url); 

                const scriptTag = `<script src="${url}" integrity="${sriHash}" crossorigin="anonymous" referrerpolicy="no-referrer"><\/script>`; 

                this.copyToClipboard(scriptTag); 

            }, 

            async copySriHash(libraryName, version, file) { 

                const url = `https://cdnjs.cloudflare.com/ajax/libs/${libraryName}/${version}/${file}`; 

                const sriHash = await this.getSriHash(url); 

                this.copyToClipboard(sriHash); 

            }, 

            async getSriHash(url) { 

                const response = await fetch(url); 

                const fileContent = await response.text(); 

                const hashBuffer = await crypto.subtle.digest('SHA-384', new TextEncoder().encode(fileContent)); 

                const hashArray = Array.from(new Uint8Array(hashBuffer)); 

                const hashBase64 = btoa(String.fromCharCode(...hashArray)); 

                return `sha384-${hashBase64}`; 

            } 

        } 

    }).mount('#app'); 