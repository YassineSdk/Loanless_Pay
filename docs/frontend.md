# Frontend Documentation

## Overview

Modern, responsive frontend for the LoanLess platform built with server-side rendering, Tailwind CSS, and progressive enhancement JavaScript.

## Architecture

### Tech Stack
- **Template Engine**: Jinja2 (Flask integration)
- **Styling**: Tailwind CSS (CDN)
- **JavaScript**: Vanilla ES6+
- **Icons**: Font Awesome 6
- **Typography**: Satoshi font
- **Design**: Mobile-first responsive

### File Structure

```
templates/
├── base.html                 # Master layout
├── landing.html              # Public homepage
├── login.html                # Authentication
├── main.html                 # User dashboard
├── profile.html              # User profile
├── loan_application/         # Loan forms
│   ├── apply.html           # Application form
│   ├── phase1_kyc.html      # KYC verification
│   ├── phase2_financial.html # Financial info
│   └── detail.html          # Application details
├── admin/                   # Admin interface
│   ├── dashboard.html       # Admin overview
│   ├── loan_applications.html # Loan management
│   └── users.html           # User management
└── funding/                 # Funding partner UI
    ├── dashboard.html       # Investment overview
    └── transactions.html    # Transaction history
```

## Design System

### Color Palette
```css
:root {
  --primary: #0a6d5d;        /* Teal brand color */
  --primary-dark: #085648;   /* Hover states */
  --accent: #f59e0b;         /* Orange highlights */
  --success: #10b981;        /* Success states */
  --error: #ef4444;          /* Error states */
  --gray-50: #f9fafb;        /* Light backgrounds */
}
```

### Typography
- **Primary Font**: Satoshi (Fontshare)
- **Headings**: Bold weights (600-700)
- **Body**: Regular weight (400)
- **Code**: Monospace fallback

### Components

#### Buttons
```html
<button class="btn-primary">Primary Action</button>
<button class="btn-secondary">Secondary Action</button>
<button class="btn-danger">Delete Action</button>
```

#### Form Inputs
```html
<input class="form-input" type="text" placeholder="Enter text">
<select class="form-select">...</select>
<textarea class="form-textarea">...</textarea>
```

#### Cards
```html
<div class="card">
  <div class="card-header">Title</div>
  <div class="card-body">Content</div>
</div>
```

## User Interface Components

### Landing Page
- Hero section with value proposition
- Feature highlights grid
- Testimonials carousel
- Call-to-action buttons
- Responsive navigation

### Loan Application Form
- Multi-step wizard interface
- Real-time validation
- Progress indicators
- File upload with drag-drop
- Calculation previews

### Admin Dashboard
- Statistics cards
- Data tables with sorting
- Filter controls
- Modal dialogs
- Action confirmations

### Funding Dashboard
- Investment metrics
- Portfolio visualization
- Transaction history
- Performance charts

## JavaScript Functionality

### Form Validation
```javascript
function validateForm() {
  const required = document.querySelectorAll('[required]');
  return Array.from(required).every(field => field.value.trim());
}
```

### File Upload
```javascript
function validateFile(file) {
  const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png'];
  const maxSize = 5 * 1024 * 1024; // 5MB
  return allowedTypes.includes(file.type) && file.size <= maxSize;
}
```

### Dynamic Content
```javascript
async function loadData(endpoint) {
  const response = await fetch(endpoint);
  return response.json();
}
```

## Responsive Design

### Breakpoints
- **Mobile**: 320px - 767px
- **Tablet**: 768px - 1023px
- **Desktop**: 1024px+

### Grid System
```css
.grid-responsive {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6;
}
```

### Mobile Optimizations
- Touch-friendly buttons (48px minimum)
- Collapsible navigation
- Optimized form layouts
- Reduced content density

## Accessibility

### ARIA Support
```html
<button aria-label="Close dialog" aria-expanded="false">
<input aria-describedby="username-help" aria-required="true">
<div role="alert" aria-live="polite">Status messages</div>
```

### Keyboard Navigation
- Tab order management
- Enter/Space key handling
- Escape key for modals
- Arrow keys for navigation

### Screen Reader Support
- Semantic HTML structure
- Descriptive alt text
- Form labels and descriptions
- Status announcements

## Performance

### Optimization Strategies
- CDN for external libraries
- Image compression and lazy loading
- Minimal JavaScript footprint
- CSS critical path optimization

### Loading States
```javascript
function showLoading() {
  document.getElementById('spinner').style.display = 'block';
}

function hideLoading() {
  document.getElementById('spinner').style.display = 'none';
}
```

## User Experience

### Navigation
- Breadcrumb trails
- Clear page hierarchy
- Contextual actions
- Back button support

### Feedback
- Success/error messages
- Progress indicators
- Loading states
- Confirmation dialogs

### Form Experience
- Inline validation
- Error highlighting
- Auto-save drafts
- Clear instructions

## Browser Support

### Compatibility
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Progressive Enhancement
- Core functionality without JavaScript
- Enhanced experience with JavaScript
- Graceful degradation

## Testing

### Manual Testing
- Cross-browser compatibility
- Responsive design verification
- Accessibility compliance
- User flow testing

### Automated Testing
```javascript
// Form validation tests
describe('Loan Application Form', () => {
  it('validates required fields', () => {
    // Test implementation
  });
});
```

## Build Process

### Development
- Live reload during development
- Source map generation
- Error overlays
- Hot module replacement

### Production
- Asset minification
- Cache busting
- Bundle optimization
- Performance monitoring