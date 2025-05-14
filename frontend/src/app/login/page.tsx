"use client";
import React from "react";

const Page = () => {
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const form = e.currentTarget;
    const name = (form.elements.namedItem("name") as HTMLInputElement).value;
    const email = (form.elements.namedItem("email") as HTMLInputElement).value;
    const password = (form.elements.namedItem("password") as HTMLInputElement).value;

    // Save to localStorage
    localStorage.setItem("user", JSON.stringify({ name, email, password }));

    // Redirect to home
    window.location.href = "/";
  };

  return (
    <div className="min-h-screen bg-neutral-900 flex items-center justify-center px-4">
      <div className="w-full max-w-sm bg-neutral-800/40 backdrop-blur-md p-8 rounded-2xl border border-neutral-700 shadow-xl">
        <h2 className="text-2xl font-semibold text-white text-center mb-6">
          Welcome Back
        </h2>
        <form className="space-y-5" onSubmit={handleSubmit}>
          <div>
            <label className="block text-sm text-white mb-1" htmlFor="name">
              Name
            </label>
            <input
              id="name"
              name="name"
              type="text"
              required
              placeholder="John Doe"
              className="w-full px-4 py-2 rounded-lg bg-neutral-800 border border-neutral-700 text-white placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-white/30"
            />
          </div>
          <div>
            <label className="block text-sm text-white mb-1" htmlFor="email">
              Email
            </label>
            <input
              id="email"
              name="email"
              type="email"
              required
              placeholder="you@example.com"
              className="w-full px-4 py-2 rounded-lg bg-neutral-800 border border-neutral-700 text-white placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-white/30"
            />
          </div>
          <div>
            <label className="block text-sm text-white mb-1" htmlFor="password">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              required
              placeholder="••••••••"
              className="w-full px-4 py-2 rounded-lg bg-neutral-800 border border-neutral-700 text-white placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-white/30"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-white text-neutral-900 font-medium py-2 rounded-lg hover:bg-neutral-200 transition"
          >
            Sign In
          </button>
        </form>
        <p className="text-center text-sm text-neutral-400 mt-6">
          Don’t have an account?{" "}
          <a href="#" className="underline hover:text-white">
            Sign up
          </a>
        </p>
      </div>
    </div>
  );
};

export default Page;
