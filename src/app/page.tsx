import Image from 'next/image';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Link from 'next/link';
import { FaLeaf, FaChartLine, FaCog } from 'react-icons/fa';

export default function HomePage() {
  return (
    <main className="min-h-screen bg-white">
      <Navbar />
      <div className="max-w-screen-full mx-auto">
        {/* Hero Section */}
        <section className="mb-24 flex flex-col p-8 md:flex-row items-center bg-gradient-to-br from-white via-green-50 to-green-100">
          <div className="md:w-1/2 p-4 text-left">
            <h1 className="text-7xl font-bold mb-8 animate-fade-in-down text-gray-800">
              Asphalt: <span className="text-green-600">Optimizing</span> Routes,
              <br />
              <span className="text-green-500">Minimizing</span> Emissions
            </h1>
            <p className="text-xl text-gray-600 animate-fade-in-up" style={{ fontFamily: 'Open Sans, sans-serif' }}>
              Experience the future of sustainable transportation with our
              cutting-edge GIS-powered route planning solutions.
            </p>
            <div className="flex space-x-4 mt-8">
              <Link href="/explore">
                <button className="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg transform transition-all hover:scale-105">
                  Explore Routes
                </button>
              </Link>
              <Link href="/">
                <button className="border-2 border-green-600 text-green-600 hover:bg-green-600 hover:text-white font-bold py-3 px-6 rounded-lg transform transition-all hover:scale-105">
                  Contact Us
                </button>
              </Link>
            </div>
          </div>

          <div className="md:w-1/2 p-4">
            <div className="relative overflow-hidden rounded-lg transform hover:scale-105 transition-transform duration-300">
              <img
                src="https://images.unsplash.com/photo-1465447142348-e9952c393450?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8cm9hZHxlbnwwfHwwfHx8MA%3D%3D"
                alt="Ithaca Commons"
                className="w-full h-[500px] object-cover rounded-lg shadow-2xl"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-gray-900 via-transparent to-transparent opacity-60"></div>
            </div>
          </div>
        </section>

        {/* Eco Section */}
        <section className="eco-section py-16 bg-gradient-to-b from-white to-green-50">
          <h2 className="text-center text-4xl font-bold mb-12 text-gray-800">
            Using <span className="text-green-600">GIS</span> for Eco-Friendly Paths
          </h2>
          <div className="flex flex-col md:flex-row justify-around space-y-8 md:space-y-0 md:space-x-8 max-w-6xl mx-auto px-4">
            <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2">
              <FaChartLine className="text-green-600 text-4xl mb-4 mx-auto" />
              <h2 className="font-semibold text-3xl mb-4 text-center text-gray-800">Real-Time Data</h2>
              <p className="text-gray-600 text-center">
                Our GIS platform integrates live traffic, weather, and
                infrastructure data to plan the most efficient routes.
              </p>
            </div>
            <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2">
              <FaLeaf className="text-green-600 text-4xl mb-4 mx-auto" />
              <h2 className="font-semibold text-3xl mb-4 text-center text-gray-800">Emissions Reduction</h2>
              <p className="text-gray-600 text-center">
                By optimizing routes, we help minimize fuel consumption and
                greenhouse gas emissions for a sustainable future.
              </p>
            </div>
            <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2">
              <FaCog className="text-green-600 text-4xl mb-4 mx-auto" />
              <h2 className="font-semibold text-3xl mb-4 text-center text-gray-800">Customizable</h2>
              <p className="text-gray-600 text-center">
                Tailor our route planning tools to your unique needs and
                preferences for maximum impact.
              </p>
            </div>
          </div>
        </section>

        {/* Container for "Get Started" and Stepper Section */}
        <div className="flex flex-col md:flex-row items-center justify-center mt-20 pb-40 bg-white text-black">
          {/* "Get Started" section */}
          <div
            id="get-started"
            className="p-4 text-left md:w-auto flex justify-center"
          >
            <div>
              <img className="h-[500px]" src="/images/image.png"></img>
              <p
                style={{ fontFamily: 'Open Sans, sans-serif' }}
                className="mt-4"
              ></p>
            </div>
          </div>

          {/* Stepper Section */}
          <section className="w-full md:w-auto ml-16">
            <h1 className="text-center text-4xl font-bold mb-8">
              Explore Our Road Network
            </h1>
            <div className="relative max-w-4xl mx-auto">
              {/* Vertical Line */}
              <div className="absolute left-5 top-0 h-full w-px bg-gray-300"></div>

              {/* Step 1 */}
              <Link href="/">
                <div className="flex items-center mb-8 relative cursor-pointer">
                  {/* Number 1 */}
                  <div className="flex-shrink-0 w-10 h-10 bg-gray-700 text-white rounded-md flex items-center justify-center text-lg font-semibold">
                    1
                  </div>

                  {/* Horizontal line to text */}
                  <div className="h-px w-16 bg-gray-300 absolute left-10 top-1/2 transform -translate-y-1/2"></div>

                  {/* Step content */}
                  <div className="ml-24">
                    <h2 className="text-3xl font-bold hover:text-gray-500 transition-colors duration-300">
                      Visualize
                    </h2>
                    <p
                      style={{ fontFamily: 'Open Sans, sans-serif' }}
                      className="mt-2 text-gray-700 transition-colors duration-300"
                    >
                      Gain a comprehensive view of the transportation
                      infrastructure in your area.
                    </p>
                  </div>
                </div>
              </Link>

              {/* Step 2 */}
              <Link href="/">
                <div className="flex items-center mb-8 relative cursor-pointer">
                  {/* Number 2 */}
                  <div className="flex-shrink-0 w-10 h-10 bg-gray-700 text-white rounded-md flex items-center justify-center text-lg font-semibold">
                    2
                  </div>

                  {/* Horizontal line to text */}
                  <div className="h-px w-16 bg-gray-300 absolute left-10 top-1/2 transform -translate-y-1/2"></div>

                  {/* Step content */}
                  <div className="ml-24">
                    <h2 className="text-3xl font-bold hover:text-gray-500 transition-colors duration-300">
                      Analyze
                    </h2>
                    <p
                      style={{ fontFamily: 'Open Sans, sans-serif' }}
                      className="mt-2 text-gray-700 transition-colors duration-300"
                    >
                      Identify bottlenecks, alternative routes, and
                      opportunities for optimization.
                    </p>
                  </div>
                </div>
              </Link>

              {/* Step 3 */}
              <Link href="/">
                <div className="flex items-center mb-8 relative cursor-pointer">
                  {/* Number 3 */}
                  <div className="flex-shrink-0 w-10 h-10 bg-gray-700 text-white rounded-md flex items-center justify-center text-lg font-semibold">
                    3
                  </div>

                  {/* Horizontal line to text */}
                  <div className="h-px w-16 bg-gray-300 absolute left-10 top-1/2 transform -translate-y-1/2"></div>

                  {/* Step content */}
                  <div className="ml-24">
                    <h2 className="text-3xl font-bold hover:text-gray-500 transition-colors duration-300">
                      Optimize
                    </h2>
                    <p
                      style={{ fontFamily: 'Open Sans, sans-serif' }}
                      className="mt-2 text-gray-700 transition-colors duration-300"
                    >
                      Plan the most efficient, eco-friendly paths for your fleet
                      or personal commute.
                    </p>
                  </div>
                </div>
              </Link>
            </div>
          </section>
        </div>
        {/* Contact Section */}
        <section className="py-16 bg-gradient-to-br from-green-50 via-green-100 to-white">
          <div className="max-w-4xl mx-auto text-center px-4">
            <h2 className="text-5xl font-bold mb-8 text-gray-800">
              Ready to <span className="text-green-600">Optimize</span> Your Routes?
            </h2>
            <p className="mb-8 text-gray-800">
              Join several other organizations already using Asphalt to reduce
              their carbon footprint.
            </p>
            <Link href="/contact">
              <button className="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-8 rounded-lg text-lg transition-colors duration-300">
                Get Started Today
              </button>
            </Link>
          </div>
        </section>

        {/* Footer */}
        <Footer />
      </div>
    </main>
  );
}

// Add these styles to your global.css
/*
@keyframes fade-in-down {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-down {
  animation: fade-in-down 1s ease-out;
}

.animate-fade-in-up {
  animation: fade-in-up 1s ease-out;
}
*/ 
