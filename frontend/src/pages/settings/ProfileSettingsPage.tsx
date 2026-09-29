export default function ProfileSettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">
          Profile & Settings
        </h1>
        <p className="mt-1 text-sm text-slate-500">
          Manage your profile information and application preferences.
        </p>
      </div>

      <section className="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
        <h2 className="text-lg font-semibold text-slate-800">
          Profile Information
        </h2>

        <div className="mt-4 space-y-3 text-sm">
          <div>
            <span className="text-slate-500">Name</span>
            <p className="font-medium text-slate-800">Demo User</p>
          </div>

          <div>
            <span className="text-slate-500">Email</span>
            <p className="font-medium text-slate-800">
              demo@mindmirror.local
            </p>
          </div>
        </div>
      </section>

      <section className="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
        <h2 className="text-lg font-semibold text-slate-800">
          Preferences
        </h2>

        <div className="mt-4 space-y-4">
          <label className="flex items-center justify-between gap-4">
            <span className="text-sm text-slate-700">
              Enable notifications
            </span>
            <input
              type="checkbox"
              className="h-4 w-4 rounded border-slate-300 text-teal-600 focus:ring-teal-500"
            />
          </label>

          <label className="flex items-center justify-between gap-4">
            <span className="text-sm text-slate-700">
              Use compact view
            </span>
            <input
              type="checkbox"
              className="h-4 w-4 rounded border-slate-300 text-teal-600 focus:ring-teal-500"
            />
          </label>
        </div>
      </section>

      <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
        <p className="text-xs text-slate-500">
          These settings are currently for UI demonstration only. They are
          not saved to an account yet.
        </p>
      </div>
    </div>
  )
}