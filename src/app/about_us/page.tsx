import Image from 'next/image';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer'
import Link from 'next/link';

export default function AboutUsPage() {

    return (
        <main className="min-h-screen bg-white">
            <Navbar />
                <div className="max-w-screen-full mx-auto">
                    <section className="overflow-auto flex flex-col p-12 md:flex-row items-center bg-gradient-to-br from-white via-green-50 to-green-100">
                        <div className="md:w-1/2 p-4 text-left">
                            <h1 className='text-5xl font-bold mb-8 animate-fade-in-down text-gray-800'>
                                Who Are We?
                            </h1>
                            <p className="text-xl text-gray-600 animate-fade-in-up" style={{ fontFamily: 'Open Sans, sans-serif' }}>
                                Lorem Ipsum
                            </p>
                        </div>

                        {/* Image Placeholder */}
                        <div className="md:w-1/2 p-4 flex justify-center">
                            <div className="relative overflow-hidden rounded-lg transform hover:scale-105 transition-transform duration-300 animate-fade-in-left">
                            <img
                                src="https://images.unsplash.com/photo-1465447142348-e9952c393450?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8cm9hZHxlbnwwfHwwfHx8MA%3D%3D"
                                alt="Ithaca Commons"
                                className="w-full h-[500px] object-cover rounded-lg shadow-2xl"
                            />
                            <div className="absolute inset-0 bg-gradient-to-t from-gray-900 via-transparent to-transparent opacity-60"></div>
                            </div>
                        </div>
                    </section>
                    <section className="flex flex-col p-12 md:flex-row items-center">
                        <div className="md:w-1/2 p-4 text-left">
                            <h1 className='text-5xl font-bold mb-8 animate-fade-in-down text-gray-800'>
                                What Do We Do?
                            </h1>
                            <p className="text-xl text-gray-600 animate-fade-in-up" style={{ fontFamily: 'Open Sans, sans-serif' }}>
                                Lorem Ipsum
                            </p>
                        </div>
                    </section>

                {/* Footer */}
                <Footer />
            </div>
        </main>
    )
}
