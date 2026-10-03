import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react'

import {
  ApiError,
  apiGet,
  apiPost,
  clearAccessToken,
  getAccessToken,
  setAccessToken,
} from '../api/client'

export interface User {
  id: number
  email: string
  full_name: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

interface TokenResponse {
  access_token: string
  token_type: string
}

interface LoginCredentials {
  email: string
  password: string
}

interface SignupData {
  email: string
  password: string
  full_name?: string
}

interface AuthContextValue {
  user: User | null
  isLoading: boolean
  isAuthenticated: boolean
  login: (credentials: LoginCredentials) => Promise<void>
  signup: (data: SignupData) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

interface AuthProviderProps {
  children: ReactNode
}

const UNAUTHORIZED_EVENT = 'mindmirror:unauthorized'

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  const logout = useCallback(() => {
    clearAccessToken()
    setUser(null)
  }, [])

  const loadCurrentUser = useCallback(async () => {
    const token = getAccessToken()

    if (!token) {
      setIsLoading(false)
      return
    }

    try {
      const currentUser = await apiGet<User>('/auth/me')
      setUser(currentUser)
    } catch {
      clearAccessToken()
      setUser(null)
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    void loadCurrentUser()
  }, [loadCurrentUser])

  useEffect(() => {
    const handleUnauthorized = () => {
      logout()
    }

    window.addEventListener(
      UNAUTHORIZED_EVENT,
      handleUnauthorized,
    )

    return () => {
      window.removeEventListener(
        UNAUTHORIZED_EVENT,
        handleUnauthorized,
      )
    }
  }, [logout])

  const login = useCallback(
    async (credentials: LoginCredentials) => {
      const tokenResponse = await apiPost<TokenResponse>(
        '/auth/login',
        credentials,
      )

      setAccessToken(tokenResponse.access_token)

      try {
        const currentUser = await apiGet<User>('/auth/me')
        setUser(currentUser)
      } catch (error) {
        clearAccessToken()
        setUser(null)
        throw error
      }
    },
    [],
  )

  const signup = useCallback(
    async (data: SignupData) => {
      await apiPost<User>('/auth/register', data)

      await login({
        email: data.email,
        password: data.password,
      })
    },
    [login],
  )

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      isLoading,
      isAuthenticated: user !== null,
      login,
      signup,
      logout,
    }),
    [user, isLoading, login, signup, logout],
  )

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }

  return context
}

export function isUnauthorizedError(error: unknown): boolean {
  return error instanceof ApiError && error.status === 401
}