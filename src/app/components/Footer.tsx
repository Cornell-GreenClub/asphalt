
import Link from 'next/link';

export default function Footer() {

    return (
        <footer className="bg-gray-50 text-gray-600 py-12">
          <div className="max-w-6xl mx-auto px-4 grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="space-y-4">
              <h3 className="text-gray-800 text-lg font-bold mb-4">Asphalt</h3>
              <p className="text-sm">
                Optimizing routes for a sustainable future.
              </p>
            </div>
            <div>
              <h4 className="text-gray-800 font-semibold mb-4">Quick Links</h4>
              <ul className="space-y-2">
                <li>
                  <Link
                    href="/explore"
                    className="hover:text-gray-800 transition-colors"
                  >
                    Explore
                  </Link>
                </li>
                <li>
                  <Link
                    href="/about"
                    className="hover:text-gray-800 transition-colors"
                  >
                    About Us
                  </Link>
                </li>
                <li>
                  <Link
                    href="/contact"
                    className="hover:text-gray-800 transition-colors"
                  >
                    Contact
                  </Link>
                </li>
              </ul>
            </div>

            <div>
              <h4 className="text-gray-800 font-semibold mb-4">Contact Us</h4>
              <p className="text-sm">Email: info@asphalt.com</p>
              <div className="mt-4 space-x-4">
                <a href="#" className="hover:text-gray-800 transition-colors">
                  Twitter
                </a>
                <a href="#" className="hover:text-gray-800 transition-colors">
                  LinkedIn
                </a>
                <a href="#" className="hover:text-gray-800 transition-colors">
                  GitHub
                </a>
              </div>
            </div>
          </div>
          <div className="max-w-6xl mx-auto px-4 mt-8 pt-8 border-t border-gray-200">
            <p className="text-sm text-center">
              © {new Date().getFullYear()} Asphalt. All rights reserved.
            </p>
          </div>
        </footer>

    )
}