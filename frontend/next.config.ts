import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // Enable standalone output for Docker production builds
  output: 'standalone',

  // Enable React Compiler (React 19)
  reactCompiler: true,

  // Disable x-powered-by header for security
  poweredByHeader: false,

  // Enable strict mode for better development experience
  reactStrictMode: true,

  // Image optimization configuration
  images: {
    remotePatterns: [
      // Add remote image domains here as needed
    ],
  },
};

export default nextConfig;
