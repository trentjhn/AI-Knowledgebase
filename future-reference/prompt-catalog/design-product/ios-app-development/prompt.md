
1. THE MASTER INFRA PROMPT
You are an expert iOS app developer who has built 10+ apps making $80K+/yr. You understand modern app architecture, clean code patterns, and scalable infrastructure.
I’m building an iOS app and need you to help me set up the infrastructure correctly from day one. Here’s what I need:
TECH STACK REQUIREMENTS:
•  Swift/SwiftUI for iOS
•  Firebase for backend (Auth, Firestore, Analytics, Crashlytics)
•  RevenueCat for subscriptions/payments
•  Superwall for paywall management
•  Clean MVVM architecture
•  Async/await for all network calls
•  Proper error handling
•  Logging system
•  Unit test setup
APP STRUCTURE: Create a scalable folder structure with:
•  Models (data models with Codable)
•  Views (SwiftUI views)
•  ViewModels (ObservableObject classes)
•  Services (API, Auth, Analytics, etc.)
•  Utilities (extensions, helpers)
•  Resources (assets, strings)
KEY SERVICES TO IMPLEMENT:
1.  AuthService - Firebase Auth with email/password and social login
2.  DatabaseService - Firestore operations with proper error handling
3.  AnalyticsService - Firebase Analytics + custom events
4.  SubscriptionService - RevenueCat integration
5.  PaywallService - Superwall integration
6.  UserService - user data management
7.  NetworkService - API calls with retry logic
CRITICAL REQUIREMENTS:
•  All services should be singletons with dependency injection
•  Implement proper loading states and error handling
•  Add analytics tracking for all user actions
•  Set up crash reporting from day one
•  Make everything testable with protocols
•  Use @StateObject and @ObservedObject correctly
•  Implement proper onboarding flow
•  Add deep linking support
•  Set up push notifications infrastructure
MONETIZATION SETUP:
•  Hard paywall after onboarding
•  RevenueCat products configuration
•  Superwall paywall triggers
•  Free trial handling
•  Restoration purchases
•  Receipt validation
ANALYTICS EVENTS TO TRACK:
•  App opens, screen views
•  Onboarding completion rate
•  Paywall shown/dismissed/converted
•  Feature usage
•  Subscription events
•  Crashes and errors
CODE PATTERNS:
•  Use async/await everywhere
•  Proper error types with localized messages
•  Loading states for all async operations
•  Offline support where possible
•  Memory management (weak self, etc.)
•  SwiftUI best practices
DEPLOYMENT SETUP:
•  Xcode project configuration
•  Bundle IDs and certificates
•  Firebase project setup
•  RevenueCat dashboard configuration
•  TestFlight beta testing
•  App Store Connect preparation
When I describe my app idea, generate the complete infrastructure code including:
1.  Project structure with all folders
2.  All service classes with full implementation
3.  Base ViewModels and Views
4.  AppDelegate/SceneDelegate setup
5.  Info.plist configuration
6.  Package.swift dependencies
7.  Firebase configuration files
8.  Example usage in main app flow
Make everything production-ready, not a tutorial. Include real error handling, proper logging, and scalable patterns I can build on. No shortcuts.



