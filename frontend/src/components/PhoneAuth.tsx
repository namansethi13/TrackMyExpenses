import { useState, useEffect } from "react"
import { Loader2, Phone, Shield } from "lucide-react"
import {
  auth,
  RecaptchaVerifier,
  signInWithPhoneNumber
} from "../firebase"

export default function PhoneLogin() {
  const [step, setStep] = useState<"phone" | "verification">("phone")
  const [countryCode, setCountryCode] = useState("+91")
  const [phoneNumber, setPhoneNumber] = useState("")
  const [verificationCode, setVerificationCode] = useState("")
  const [confirmationResult, setConfirmationResult] = useState<any | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")
  const [message, setMessage] = useState("")

  useEffect(() => {
    if (!(window as any).recaptchaVerifier) {
      (window as any).recaptchaVerifier = new RecaptchaVerifier(
        auth,
        "recaptcha-container",
        {
          size: "invisible",
          callback: () => console.log("Recaptcha Verified"),
        }
      )
    }
  }, [])

  const handlePhoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPhoneNumber(e.target.value)
    setError("")
  }

  const handleSendCode = async () => {
    const fullPhone = `${countryCode}${phoneNumber.replace(/\D/g, "")}`
    const digitsOnly = fullPhone.replace(/\D/g, "")

    if (!fullPhone || digitsOnly.length < 10) {
      setError(`Please enter a valid phone number for ${countryCode}`)
      return
    }

    setIsLoading(true)
    setError("")
    setMessage("")

    try {
      const appVerifier = (window as any).recaptchaVerifier
      const result = await signInWithPhoneNumber(auth, fullPhone, appVerifier)
      setConfirmationResult(result)
      setStep("verification")
      setMessage("OTP sent!")
    } catch (err) {
      console.error(err)
      setError("Failed to send OTP. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  const handleVerificationCodeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setVerificationCode(e.target.value.replace(/\D/g, "").slice(0, 6))
    setError("")
  }

  const handleLogin = async () => {
    if (verificationCode.length !== 6 || !confirmationResult) {
      setError("Please enter the complete 6-digit verification code")
      return
    }

    setIsLoading(true)
    setError("")

    try {
      await confirmationResult.confirm(verificationCode)
      setMessage("Phone number verified!")
      alert("Login successful!")
    } catch (err) {
      console.error(err)
      setError("Invalid verification code. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  const handleResendCode = async () => {
    setStep("phone")
    setVerificationCode("")
    setError("")
    setMessage("")
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="w-full max-w-md bg-white rounded-lg shadow-lg border border-gray-200">
        {/* Header */}
        <div className="text-center p-6 pb-4">
          <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-blue-100">
            {step === "phone" ? (
              <Phone className="h-6 w-6 text-blue-600" />
            ) : (
              <Shield className="h-6 w-6 text-blue-600" />
            )}
          </div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            {step === "phone" ? "Sign in with Phone" : "Verify Your Phone"}
          </h1>
          <p className="text-gray-600 text-sm">
            {step === "phone"
              ? "Enter your phone number to receive a verification code"
              : `We sent a 6-digit code to ${countryCode} ${phoneNumber}`}
          </p>
        </div>

        {/* Content */}
        <div className="p-6 pt-0 space-y-4">
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-md p-3">
              <p className="text-red-800 text-sm">{error}</p>
            </div>
          )}
          {message && (
            <div className="bg-green-50 border border-green-200 rounded-md p-3">
              <p className="text-green-800 text-sm">{message}</p>
            </div>
          )}

          {step === "phone" ? (
            <div className="space-y-4">
              <div className="space-y-2">
                <label htmlFor="phone" className="block text-sm font-medium text-gray-700">
                  Phone Number
                </label>
                <div className="flex gap-2">
                  <select
                    value={countryCode}
                    onChange={(e) => setCountryCode(e.target.value)}
                    className="w-32 px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white text-sm"
                  >
                    <option value="+91">India +91</option>
                  </select>
                  <input
                    id="phone"
                    type="tel"
                    placeholder="1234567890"
                    value={phoneNumber}
                    onChange={handlePhoneChange}
                    className="flex-1 px-3 py-2 text-lg border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                  />
                </div>
                <p className="text-sm text-gray-500">
                  We'll send you a verification code via SMS
                </p>
              </div>
              <button
                onClick={handleSendCode}
                disabled={isLoading}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-md transition-colors duration-200 flex items-center justify-center"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Sending Code...
                  </>
                ) : (
                  "Send Code"
                )}
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="space-y-2">
                <label htmlFor="code" className="block text-sm font-medium text-gray-700">
                  Verification Code
                </label>
                <input
                  id="code"
                  type="text"
                  placeholder="123456"
                  value={verificationCode}
                  onChange={handleVerificationCodeChange}
                  className="w-full px-3 py-2 text-lg text-center tracking-widest border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                  maxLength={6}
                />
                <p className="text-sm text-gray-500">
                  Enter the 6-digit code sent to your phone
                </p>
              </div>

              <button
                onClick={handleLogin}
                disabled={isLoading}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-md transition-colors duration-200 flex items-center justify-center"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Verifying...
                  </>
                ) : (
                  "Login"
                )}
              </button>

              <div className="text-center space-y-2">
                <p className="text-sm text-gray-500">Didn't receive the code?</p>
                <div className="flex flex-col sm:flex-row gap-2">
                  <button
                    onClick={handleSendCode}
                    disabled={isLoading}
                    className="flex-1 bg-white hover:bg-gray-50 text-gray-700 font-medium py-2 px-4 rounded-md border border-gray-300"
                  >
                    Resend Code
                  </button>
                  <button
                    onClick={handleResendCode}
                    className="flex-1 bg-transparent hover:bg-gray-50 text-gray-600 font-medium py-2 px-4 rounded-md"
                  >
                    Change Number
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
        <div id="recaptcha-container" />
      </div>
    </div>
  )
}
