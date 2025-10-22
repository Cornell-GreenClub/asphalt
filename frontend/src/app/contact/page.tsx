'use client';

import { useState } from 'react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { Poppins } from 'next/font/google';

const poppins = Poppins({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
});

interface FormData {
  fullName: string;
  email: string;
  phone: string;
  message: string;
}

const ContactInput = ({ 
  type, 
  name, 
  value, 
  onChange, 
  placeholder, 
  required
}: { 
  type: string;
  name: keyof FormData;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void;
  placeholder: string;
  required?: boolean;
}) => {
  const isTextArea = type === 'textarea';
  const InputComponent = isTextArea ? 'textarea' : 'input';
  const inputId = `contact-${name}`;
  
  return (
    <div>
      <label htmlFor={inputId} className="sr-only">
        {placeholder}
      </label>
      <InputComponent
        id={inputId}
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        rows={isTextArea ? 4 : undefined}
        className="w-full px-4 py-2 border border-gray-400 rounded-md focus:outline-none focus:ring-2 focus:ring-[#034626] text-gray-700 placeholder-gray-600 text-base poppins-regular"
        style={isTextArea ? { resize: 'none', overflowY: 'auto' } : undefined}
      />
    </div>
  );
};

export default function ContactPage() {
  const [formData, setFormData] = useState<FormData>({
    fullName: '',
    email: '',
    phone: '',
    message: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <>
      <main className={`min-h-screen bg-white ${poppins.className}`}>
        <Navbar />
        <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-green-50 p-2 md:p-6">
          <div className="max-w-7xl mx-auto grid md:grid-cols-2 gap-24 items-stretch mt-16">
            <div className="w-full flex flex-col h-full justify-end">
              <div>
                <div className="aspect-[3/2] w-full relative overflow-hidden rounded-lg transform hover:scale-105 transition-transform duration-300">
                  <img
                    src="/images/road.jpeg"
                    alt="Winding road through forest"
                    className="w-full h-full object-cover rounded-lg shadow-2xl"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-gray-900 via-transparent to-transparent opacity-60"></div>
                </div>
                <p className="mt-4 text-base text-gray-700 poppins-regular font-normal">
                  Have a question or want to get in touch? Just fill out the form or{' '}
                  <a href="mailto:info@asphalt.com" className="asphalt-green asphalt-green-hover underline poppins-regular">
                    shoot us an email
                  </a>
                  —we'd love to hear from you!
                </p>
              </div>
            </div>

            <div className="w-full flex flex-col">
              <h1 className="text-[52px] poppins-semibold mb-4 text-gray-900">Contact Us</h1>
              <form className="space-y-6">
                <ContactInput
                  type="text"
                  name="fullName"
                  value={formData.fullName}
                  onChange={handleChange}
                  placeholder="Full Name*"
                  required
                />
                <ContactInput
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="Email Address*"
                  required
                />
                <ContactInput
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleChange}
                  placeholder="Phone Number"
                />
                <ContactInput
                  type="textarea"
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  placeholder="Message*"
                  required
                />
                <button
                  type="button"
                  className="bg-[#034626] hover:bg-[#023219] text-white px-8 py-3 rounded-2xl text-base poppins-bold transform transition-all hover:scale-105"
                >
                  Submit
                </button>
              </form>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
} 