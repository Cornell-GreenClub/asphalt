import type { Metadata } from 'next';
import localFont from 'next/font/local';
import './globals.css';

const poppins = localFont({
  src: './fonts/Poppins/Poppins-Regular.ttf',
  variable: '--font-poppins-regular',
});

const poppinsBold = localFont({
  src: './fonts/Poppins/Poppins-Bold.ttf',
  variable: '--font-poppins-bold',
});

const poppinsMedium = localFont({
  src: './fonts/Poppins/Poppins-Medium.ttf',
  variable: '--font-poppins-medium',
});

const poppinsExtraBold = localFont({
  src: './fonts/Poppins/Poppins-ExtraBold.ttf',
  variable: '--font-poppins-extrabold',
});

const poppinsSemibold = localFont({
  src: './fonts/Poppins/Poppins-SemiBold.ttf',
  variable: '--font-poppins-semibold',
});

export const metadata: Metadata = {
  title: 'Asphalt',
  description: 'Smarter routes, greener future',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
      <html lang="en">
        <body
          className={`${poppins.variable} ${poppinsBold.variable} ${poppinsMedium.variable} ${poppinsExtraBold.variable} ${poppinsSemibold.variable} antialiased`}
        >
          {children}
        </body>
      </html>
    </>
  );
}
