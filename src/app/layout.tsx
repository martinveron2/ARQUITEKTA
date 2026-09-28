import type { Metadata, Viewport } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'ARQUITEKTA',
  description: 'La base de diseño de tu futura app',
  manifest: '/manifest.webmanifest'
};
export const viewport: Viewport = { width: 'device-width', initialScale: 1, themeColor: '#5B35F5' };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="es"><body>{children}</body></html>;
}
