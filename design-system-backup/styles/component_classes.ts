// Reusable component classes based on design system
// These can be customized based on your external ideation

export const componentClasses = {
  // Button variants
  button: {
    base: 'inline-flex items-center justify-center font-medium rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed',
    primary: 'bg-primary-600 hover:bg-primary-700 text-white focus:ring-primary-500 shadow-sm hover:shadow-md',
    secondary: 'bg-secondary-100 hover:bg-secondary-200 text-secondary-900 focus:ring-secondary-500',
    outline: 'border border-secondary-300 hover:bg-secondary-50 text-secondary-700 focus:ring-primary-500 bg-white',
    ghost: 'hover:bg-secondary-100 text-secondary-700 focus:ring-secondary-500',
    danger: 'bg-accent-error hover:bg-red-600 text-white focus:ring-red-500',
    success: 'bg-accent-success hover:bg-green-600 text-white focus:ring-green-500',
    sizes: {
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-4 py-2 text-base',
      lg: 'px-6 py-3 text-lg',
      xl: 'px-8 py-4 text-xl',
    }
  },

  // Card variants
  card: {
    base: 'bg-white rounded-xl border border-secondary-200 shadow-soft hover:shadow-medium transition-shadow duration-200',
    elevated: 'bg-white rounded-xl shadow-medium hover:shadow-large transition-shadow duration-200',
    outlined: 'bg-white rounded-xl border-2 border-secondary-200 hover:border-primary-300 transition-colors duration-200',
    flat: 'bg-secondary-50 rounded-xl border border-secondary-100',
    sizes: {
      sm: 'p-4',
      md: 'p-6',
      lg: 'p-8',
    }
  },

  // Input variants
  input: {
    base: 'w-full px-3 py-2 border border-secondary-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors duration-200 placeholder-secondary-400',
    error: 'border-accent-error focus:ring-red-500',
    success: 'border-accent-success focus:ring-green-500',
    sizes: {
      sm: 'px-2 py-1 text-sm',
      md: 'px-3 py-2 text-base',
      lg: 'px-4 py-3 text-lg',
    }
  },

  // Typography classes
  typography: {
    heading: {
      h1: 'text-4xl md:text-5xl lg:text-6xl font-bold text-secondary-900 leading-tight',
      h2: 'text-3xl md:text-4xl lg:text-5xl font-bold text-secondary-900 leading-tight',
      h3: 'text-2xl md:text-3xl font-semibold text-secondary-900 leading-tight',
      h4: 'text-xl md:text-2xl font-semibold text-secondary-900 leading-tight',
      h5: 'text-lg md:text-xl font-medium text-secondary-900 leading-tight',
      h6: 'text-base md:text-lg font-medium text-secondary-900 leading-tight',
    },
    body: {
      large: 'text-lg text-secondary-700 leading-relaxed',
      base: 'text-base text-secondary-700 leading-relaxed',
      small: 'text-sm text-secondary-600 leading-relaxed',
      caption: 'text-xs text-secondary-500 leading-relaxed',
    }
  },

  // Layout classes
  layout: {
    container: 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8',
    containerSm: 'max-w-4xl mx-auto px-4 sm:px-6 lg:px-8',
    containerLg: 'max-w-8xl mx-auto px-4 sm:px-6 lg:px-8',
    section: 'py-16 lg:py-24',
    sectionSm: 'py-8 lg:py-12',
    sectionLg: 'py-24 lg:py-32',
  },

  // Grid classes
  grid: {
    auto: 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8',
    features: 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8',
    cards: 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6',
    masonry: 'columns-1 md:columns-2 lg:columns-3 gap-6',
  },

  // Animation classes
  animation: {
    fadeIn: 'animate-fade-in',
    slideUp: 'animate-slide-up',
    bounceGentle: 'animate-bounce-gentle',
    hover: 'hover:scale-105 hover:shadow-lg transition-all duration-200',
    focus: 'focus:scale-105 focus:shadow-lg transition-all duration-200',
  },

  // Background variants
  background: {
    gradient: 'bg-gradient-to-br from-primary-50 to-secondary-50',
    gradientDark: 'bg-gradient-to-br from-secondary-800 to-secondary-900',
    pattern: 'bg-white bg-opacity-90 backdrop-blur-sm',
    glass: 'bg-white bg-opacity-10 backdrop-blur-md border border-white border-opacity-20',
  }
} as const;

// Utility function to combine classes
export const cn = (...classes: (string | undefined | null | false)[]): string => {
  return classes.filter(Boolean).join(' ');
};

// Specific component combinations
export const buttonVariants = {
  primary: cn(componentClasses.button.base, componentClasses.button.primary),
  secondary: cn(componentClasses.button.base, componentClasses.button.secondary),
  outline: cn(componentClasses.button.base, componentClasses.button.outline),
  ghost: cn(componentClasses.button.base, componentClasses.button.ghost),
  danger: cn(componentClasses.button.base, componentClasses.button.danger),
  success: cn(componentClasses.button.base, componentClasses.button.success),
} as const;

export const cardVariants = {
  default: cn(componentClasses.card.base),
  elevated: cn(componentClasses.card.elevated),
  outlined: cn(componentClasses.card.outlined),
  flat: cn(componentClasses.card.flat),
} as const;
