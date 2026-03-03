"use client";

export default function LoadingState() {
  return (
    <div className="w-full flex flex-col items-center gap-6 py-8 animate-pulse">
      {[1, 2, 3, 4, 5].map((i) => (
        <div key={i} className="flex flex-col items-center gap-4">
          <div
            className="bg-gray-800 border-2 border-gray-700 rounded-xl px-5 py-4 w-72"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="h-4 w-16 bg-gray-700 rounded" />
              <div className="h-4 w-14 bg-gray-700 rounded-full" />
            </div>
            <div className="space-y-2">
              <div className="h-3 w-full bg-gray-700 rounded" />
              <div className="h-3 w-3/4 bg-gray-700 rounded" />
            </div>
          </div>
          {i < 5 && (
            <div className="h-8 w-0.5 bg-gray-700 rounded" />
          )}
        </div>
      ))}
      <p className="text-gray-500 text-sm mt-2">
        Simulating butterfly effects... this may take 10-15 seconds
      </p>
    </div>
  );
}
