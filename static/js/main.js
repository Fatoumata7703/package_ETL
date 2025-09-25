// ===========================================
// ETL CACAO - JAVASCRIPT MAGIQUE
// ===========================================

// Configuration
const CONFIG = {
    apiBaseUrl: '/api',
    datasets: {
        raw: 'cacao_raw.csv',
        interim: 'cacao_interim.csv', 
        clean: 'cacao_clean.csv'
    }
};

// État de l'application
const AppState = {
    currentDataset: null,
    isLoading: false,
    datasets: {
        raw: null,
        interim: null,
        clean: null
    }
};

// ===========================================
// INITIALISATION
// ===========================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🍫 ETL Cacao - Initialisation...');
    
    initializeApp();
    setupEventListeners();
    loadDatasetStats();
    setupSmoothScrolling();
    setupAnimations();
});

function initializeApp() {
    // Ajouter des classes d'animation
    document.body.classList.add('loaded');
    
    // Initialiser les tooltips
    initializeTooltips();
    
    // Charger les statistiques des datasets
    loadDatasetStats();
}

// ===========================================
// EVENT LISTENERS
// ===========================================

function setupEventListeners() {
    // Navigation
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', handleNavClick);
    });
    
    // Boutons de téléchargement
    const downloadBtns = document.querySelectorAll('[onclick*="downloadDataset"]');
    downloadBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const datasetType = this.getAttribute('onclick').match(/'([^']+)'/)[1];
            downloadDataset(datasetType);
        });
    });
    
    // Boutons de visualisation
    const viewBtns = document.querySelectorAll('[onclick*="viewDataset"]');
    viewBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const datasetType = this.getAttribute('onclick').match(/'([^']+)'/)[1];
            viewDataset(datasetType);
        });
    });
    
    // Fermeture du modal
    const modalClose = document.querySelector('.modal-close');
    if (modalClose) {
        modalClose.addEventListener('click', closeModal);
    }
    
    // Fermeture du modal en cliquant à l'extérieur
    const modal = document.getElementById('datasetModal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeModal();
            }
        });
    }
    
    // Scroll pour la navigation
    window.addEventListener('scroll', handleScroll);
}

function handleNavClick(e) {
    const href = this.getAttribute('href') || '';
    // Si ce n'est pas un lien ancre (#...), laisser la navigation normale
    if (!href.startsWith('#')) {
        return; // ne pas empêcher le comportement par défaut
    }
    
    e.preventDefault();
    const targetId = href.substring(1);
    const targetElement = document.getElementById(targetId);
    
    if (targetElement) {
        // Mettre à jour la navigation active
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        this.classList.add('active');
        
        // Scroll vers la section
        targetElement.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

function handleScroll() {
    const nav = document.querySelector('.main-nav');
    const scrollY = window.scrollY;
    
    if (scrollY > 100) {
        nav.style.background = 'rgba(255, 255, 255, 0.98)';
        nav.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
    } else {
        nav.style.background = 'rgba(255, 255, 255, 0.95)';
        nav.style.boxShadow = 'none';
    }
    
    // Mise à jour de la navigation active basée sur le scroll
    updateActiveNavLink();
}

function updateActiveNavLink() {
    const sections = ['datasets', 'pipeline', 'transformations'];
    const navLinks = document.querySelectorAll('.nav-link');
    
    let currentSection = '';
    
    sections.forEach(sectionId => {
        const section = document.getElementById(sectionId);
        if (section) {
            const rect = section.getBoundingClientRect();
            if (rect.top <= 100 && rect.bottom >= 100) {
                currentSection = sectionId;
            }
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${currentSection}`) {
            link.classList.add('active');
        }
    });
}

// ===========================================
// FONCTIONS DATASET
// ===========================================

async function loadDatasetStats() {
    console.log('📊 Chargement des statistiques des datasets...');
    
    try {
        // Simuler le chargement des statistiques
        const stats = {
            raw: { rows: 1795, cols: 9, size: '126.3 KB' },
            interim: { rows: 1795, cols: 9, size: '128.7 KB' },
            clean: { rows: 1795, cols: 9, size: '131.2 KB' }
        };
        
        // Mettre à jour l'interface seulement si les éléments existent
        Object.keys(stats).forEach(datasetType => {
            const stat = stats[datasetType];
            const rowsElement = document.getElementById(`${datasetType}-rows`);
            const colsElement = document.getElementById(`${datasetType}-cols`);
            const sizeElement = document.getElementById(`${datasetType}-size`);
            
            if (rowsElement) rowsElement.textContent = stat.rows.toLocaleString();
            if (colsElement) colsElement.textContent = stat.cols;
            if (sizeElement) sizeElement.textContent = stat.size;
        });
        
        console.log('✅ Statistiques chargées avec succès');
        
    } catch (error) {
        console.error('❌ Erreur lors du chargement des statistiques:', error);
        // Ne pas afficher l'erreur si on n'est pas sur la page datasets
        if (document.getElementById('raw-rows')) {
            showNotification('Erreur lors du chargement des statistiques', 'error');
        }
    }
}

async function viewDataset(datasetType) {
    console.log(`👁️ Visualisation du dataset: ${datasetType}`);
    
    if (AppState.isLoading) return;
    
    AppState.isLoading = true;
    AppState.currentDataset = datasetType;
    
    try {
        // Afficher le modal
        const modal = document.getElementById('datasetModal');
        const modalTitle = document.getElementById('modalTitle');
        const datasetPreview = document.getElementById('datasetPreview');
        
        modalTitle.textContent = `Dataset ${datasetType.toUpperCase()}`;
        
        // Afficher un loader
        datasetPreview.innerHTML = `
            <div class="loading-container" style="text-align: center; padding: 2rem;">
                <div class="loading-spinner"></div>
                <p>Chargement du dataset...</p>
            </div>
        `;
        
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
        
        // Simuler le chargement des données
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Afficher les données
        const sampleData = generateSampleData(datasetType);
        datasetPreview.innerHTML = `
            <div class="dataset-preview">
                <div class="preview-header">
                    <h4>${CONFIG.datasets[datasetType]}</h4>
                    <div class="preview-stats">
                        <span class="stat">1795 lignes</span>
                        <span class="stat">9 colonnes</span>
                        <span class="stat">131.2 KB</span>
                    </div>
                </div>
                <div class="preview-table">
                    ${generateTableHTML(sampleData)}
                </div>
                <div class="preview-actions">
                    <button class="btn btn-primary" onclick="downloadDataset('${datasetType}')">
                        <i class="fas fa-download"></i>
                        Télécharger CSV
                    </button>
                </div>
            </div>
        `;
        
    } catch (error) {
        console.error('❌ Erreur lors de la visualisation:', error);
        showNotification('Erreur lors de la visualisation du dataset', 'error');
    } finally {
        AppState.isLoading = false;
    }
}

function generateSampleData(datasetType) {
    const baseData = [
        { Company: 'A. Morin', 'Origine spécifique': 'Agua Grande', REF: 1876, 'Date de la revue': 2016, 'Pourcentage de cacao': 63.0, 'Localisation': 'France', Note: 3.75, 'Type de fève': 'Sao Tome', 'Broad Bean Origin': 'Sao Tome' },
        { Company: 'A. Morin', 'Origine spécifique': 'Kpime', REF: 1676, 'Date de la revue': 2015, 'Pourcentage de cacao': 70.0, 'Localisation': 'France', Note: 2.75, 'Type de fève': 'Togo', 'Broad Bean Origin': 'Togo' },
        { Company: 'A. Morin', 'Origine spécifique': 'Atsane', REF: 1676, 'Date de la revue': 2015, 'Pourcentage de cacao': 70.0, 'Localisation': 'France', Note: 3.00, 'Type de fève': 'Togo', 'Broad Bean Origin': 'Togo' },
        { Company: 'A. Morin', 'Origine spécifique': 'Akata', REF: 1680, 'Date de la revue': 2015, 'Pourcentage de cacao': 70.0, 'Localisation': 'France', Note: 3.50, 'Type de fève': 'Togo', 'Broad Bean Origin': 'Togo' },
        { Company: 'A. Morin', 'Origine spécifique': 'Quilla', REF: 1704, 'Date de la revue': 2015, 'Pourcentage de cacao': 70.0, 'Localisation': 'France', Note: 3.50, 'Type de fève': 'Peru', 'Broad Bean Origin': 'Peru' }
    ];
    
    // Modifier les données selon le type de dataset
    if (datasetType === 'raw') {
        // Données brutes - avec des problèmes
        return baseData.map(row => ({
            ...row,
            'Type de fève': Math.random() > 0.5 ? row['Type de fève'] : null,
            'Broad Bean Origin': Math.random() > 0.9 ? null : row['Broad Bean Origin']
        }));
    } else if (datasetType === 'interim') {
        // Données intermédiaires - nettoyées mais pas encore imputées
        return baseData.map(row => ({
            ...row,
            'Type de fève': Math.random() > 0.5 ? row['Type de fève'] : null,
            'Broad Bean Origin': row['Broad Bean Origin']
        }));
    } else {
        // Données finales - complètement nettoyées
        return baseData.map(row => ({
            ...row,
            'Type de fève': row['Type de fève'] || 'Unknown',
            'Broad Bean Origin': row['Broad Bean Origin'] || 'Venezuela'
        }));
    }
}

function generateTableHTML(data) {
    if (!data || data.length === 0) {
        return '<p>Aucune donnée disponible</p>';
    }
    
    const headers = Object.keys(data[0]);
    const rows = data.slice(0, 10); // Limiter à 10 lignes pour l'aperçu
    
    let html = '<table class="preview-table-content">';
    
    // En-têtes
    html += '<thead><tr>';
    headers.forEach(header => {
        html += `<th>${header}</th>`;
    });
    html += '</tr></thead>';
    
    // Données
    html += '<tbody>';
    rows.forEach(row => {
        html += '<tr>';
        headers.forEach(header => {
            const value = row[header];
            html += `<td>${value !== null ? value : '<span class="null-value">-</span>'}</td>`;
        });
        html += '</tr>';
    });
    html += '</tbody>';
    
    html += '</table>';
    
    if (data.length > 10) {
        html += `<p class="preview-note">Aperçu des 10 premières lignes sur ${data.length} total</p>`;
    }
    
    return html;
}

function downloadDataset(datasetType) {
    console.log(`📥 Téléchargement du dataset: ${datasetType}`);
    
    const filename = CONFIG.datasets[datasetType];
    const downloadUrl = `${CONFIG.apiBaseUrl}/download/${datasetType}`;
    
    // Créer un lien de téléchargement temporaire
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = filename;
    link.style.display = 'none';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showNotification(`Téléchargement de ${filename} démarré`, 'success');
}

function closeModal() {
    const modal = document.getElementById('datasetModal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
    AppState.currentDataset = null;
}

// ===========================================
// ANIMATIONS ET EFFETS
// ===========================================

function setupAnimations() {
    // Animation d'apparition des cartes avec effet premium
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0) scale(1)';
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observer les cartes et éléments premium
    const animatedElements = document.querySelectorAll('.dataset-card, .pipeline-step, .transformation-card, .stat-item, .premium-badge');
    animatedElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px) scale(0.95)';
        element.style.transition = `opacity 0.8s cubic-bezier(0.4, 0, 0.2, 1) ${index * 0.1}s, transform 0.8s cubic-bezier(0.4, 0, 0.2, 1) ${index * 0.1}s`;
        observer.observe(element);
    });
    
    // Animation des particules de cacao
    animateCocoaParticles();
    
    // Animation des orbes de gradient
    animateGradientOrbs();
}

function animateCocoaParticles() {
    const particles = document.querySelectorAll('.cocoa-particle');
    particles.forEach((particle, index) => {
        // Animation aléatoire pour chaque particule
        const randomDelay = Math.random() * 2;
        const randomDuration = 4 + Math.random() * 4;
        
        particle.style.animationDelay = `${randomDelay}s`;
        particle.style.animationDuration = `${randomDuration}s`;
    });
}

function animateGradientOrbs() {
    const orbs = document.querySelectorAll('.orb');
    orbs.forEach((orb, index) => {
        // Animation différente pour chaque orbe
        const randomDelay = Math.random() * 3;
        const randomDuration = 6 + Math.random() * 4;
        
        orb.style.animationDelay = `${randomDelay}s`;
        orb.style.animationDuration = `${randomDuration}s`;
    });
}

function setupSmoothScrolling() {
    // Smooth scrolling pour tous les liens internes
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ===========================================
// NOTIFICATIONS
// ===========================================

function showNotification(message, type = 'info') {
    // Créer l'élément de notification
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${getNotificationIcon(type)}"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Styles pour la notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 300px;
    `;
    
    document.body.appendChild(notification);
    
    // Animation d'entrée
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Supprimer après 3 secondes
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

function getNotificationIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function getNotificationColor(type) {
    const colors = {
        success: '#27AE60',
        error: '#E74C3C',
        warning: '#F39C12',
        info: '#3498DB'
    };
    return colors[type] || '#3498DB';
}

// ===========================================
// TOOLTIPS
// ===========================================

function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(e) {
    const text = e.target.getAttribute('data-tooltip');
    if (!text) return;
    
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = text;
    tooltip.style.cssText = `
        position: absolute;
        background: #333;
        color: white;
        padding: 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.875rem;
        z-index: 1000;
        pointer-events: none;
        white-space: nowrap;
    `;
    
    document.body.appendChild(tooltip);
    
    const rect = e.target.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
    
    e.target._tooltip = tooltip;
}

function hideTooltip(e) {
    if (e.target._tooltip) {
        e.target._tooltip.remove();
        delete e.target._tooltip;
    }
}

// ===========================================
// UTILITAIRES
// ===========================================

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ===========================================
// EXPORT POUR USAGE GLOBAL
// ===========================================

window.ETLCacao = {
    viewDataset,
    downloadDataset,
    closeModal,
    showNotification
};

console.log('🍫 ETL Cacao - JavaScript chargé avec succès!');