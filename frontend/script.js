// Cache DOM elements
const form = document.getElementById('url-form');
const urlInput = document.getElementById('url-input');
const feedback = document.getElementById('feedback');
const linksContainer = document.getElementById("download-links");
const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
const navLinks = document.querySelector('.nav-links');

// Cache for API responses
const apiCache = new Map();

// Debounce function
const debounce = (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

// Mobile menu toggle with event delegation
document.addEventListener('click', (e) => {
    if (e.target.closest('.mobile-menu-btn')) {
        navLinks.classList.toggle('active');
        const icon = mobileMenuBtn.querySelector('i');
        icon.classList.toggle('fa-bars');
        icon.classList.toggle('fa-times');
    }
});

// Close mobile menu when clicking outside
document.addEventListener('click', (e) => {
    if (!navLinks.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
        navLinks.classList.remove('active');
        const icon = mobileMenuBtn.querySelector('i');
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
    }
});

// Close mobile menu when clicking a link
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        const icon = mobileMenuBtn.querySelector('i');
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
    });
});

// Optimized FAQ accordion with event delegation
document.querySelector('.faq-container').addEventListener('click', (e) => {
    const question = e.target.closest('.faq-question');
    if (!question) return;

    const answer = question.nextElementSibling;
    const isActive = question.classList.contains('active');

    // Close all other answers
    document.querySelectorAll('.faq-question').forEach(q => {
        if (q !== question) {
            q.classList.remove('active');
            q.nextElementSibling.classList.remove('active');
        }
    });

    // Toggle current answer
    question.classList.toggle('active');
    answer.classList.toggle('active');
});

// Create download card with optimized DOM manipulation
function createDownloadCard(video, container) {
    const fragment = document.createDocumentFragment();

    // Create thumbnail
    const img = document.createElement('img');
    img.src = video.thumbnail;
    img.alt = 'Thumbnail';
    img.loading = 'lazy';
    fragment.appendChild(img);

    // Create formats container
    const formatsContainer = document.createElement('div');
    formatsContainer.className = "formats";

    // Add format links
    const formats = video.formats || [];
    formats.forEach(format => {
        if (format.protocol === "https") {
            const downloadLink = document.createElement("a");
            downloadLink.href = format.url;
            const filesize = format.filesize_approx / (1024 * 1024);
            downloadLink.textContent = `⬇️ ${format.resolution ? format.resolution + " " : ""} ≈ ${Math.round(filesize)} MB`;
            downloadLink.className = "format-link";
            downloadLink.download = "";
            downloadLink.target = "_blank";
            formatsContainer.appendChild(downloadLink);
        }
    });

    fragment.appendChild(formatsContainer);
    container.appendChild(fragment);
}

// Debounced form submission
const debouncedSubmit = debounce(async (e) => {
    e.preventDefault();
    linksContainer.innerHTML = '';
    const twitterUrl = urlInput.value.trim();

    if (!twitterUrl) {
        feedback.textContent = 'Please enter a valid Twitter video URL.';
        return;
    }

    // Show loading state
    feedback.textContent = 'Processing...';
    form.classList.add('loading');

    try {
        // Check cache first
        if (apiCache.has(twitterUrl)) {
            const cachedData = apiCache.get(twitterUrl);
            handleResponse(cachedData);
            return;
        }

        const response = await fetchWithTimeout('http://localhost:8000/download/twitter', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: twitterUrl })
        }, 5000);

        const data = await response.json();

        if (response.ok) {
            // Cache successful response
            apiCache.set(twitterUrl, data);
            handleResponse(data);
        } else {
            feedback.textContent = data.error || 'An error occurred while processing the request.';
        }
    } catch (error) {
        console.error('Error:', error);
        feedback.textContent = 'Something went wrong. Please try again later.';
    } finally {
        form.classList.remove('loading');
    }
}, 300);

// Add event listener with debounce
form.addEventListener('submit', debouncedSubmit);

// Handle API response
function handleResponse(data) {
    if (data._type === 'playlist') {
        const entries = data.entries || [];
        entries.forEach(entry => {
            const entryContainer = document.createElement('div');
            entryContainer.className = 'entry-container';
            linksContainer.appendChild(entryContainer);
            createDownloadCard(entry, entryContainer);
        });
        feedback.textContent = `Playlist with ${entries.length} videos loaded successfully!`;
    } else {
        const singleContainer = document.createElement('div');
        singleContainer.className = 'single-entry-container';
        linksContainer.appendChild(singleContainer);
        createDownloadCard(data, singleContainer);
        feedback.textContent = 'Video loaded successfully!';
    }
}

// Fetch with timeout
async function fetchWithTimeout(url, options, timeoutMs = 5000) {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeoutMs);
    try {
        const response = await fetch(url, { ...options, signal: controller.signal });
        clearTimeout(id);
        return response;
    } catch (error) {
        clearTimeout(id);
        throw error;
    }
}

// Intersection Observer for lazy loading
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            observer.unobserve(img);
        }
    });
}, {
    rootMargin: '50px 0px',
    threshold: 0.1
});

// Observe all images
document.querySelectorAll('img[data-src]').forEach(img => observer.observe(img));