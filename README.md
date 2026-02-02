
## 🎯 Project Overview

**Samrtbook** is a digital ledger/credit management system similar to popular apps like Khatabook, OkCredit. It helps businesses:
- Track customer credit/debit transactions
- Maintain running balances for each customer
- Send automated SMS reminders for dues
- Attach proof images to transactions
- Generate customer statements

**Tech Stack:**
- **Backend:** Django + Django REST Framework
- **Database:** SQLite (can be upgraded to PostgreSQL)
- **SMS Service:** Twilio integration
- **File Upload:** Image proof storage

---

## 🏗️ Backend Architecture Summary

### Core Apps
- **reminders** - Main app containing all models and business logic

### Key Features
- ✅ Customer management
- ✅ Transaction recording (Credit/Debit)
- ✅ Running balance calculation
- ✅ Image proof upload for transactions
- ✅ SMS notifications (Twilio)
- ✅ Customer statement generation
- ✅ Manual reminder sending
- ✅ CORS enabled for frontend
- ✅ Cron job support for automated reminders

---

## 🔌 API Endpoints Reference

### Base URL
```
http://localhost:8000/api/
```

### 1. **Customer Management**

#### **GET /api/customers/**
Get all customers (ordered by newest first)

**Response:**
```json
[
  {
    "id": 1,
    "name": "Rahul Sharma",
    "phone": "+919876543210",
    "email": "rahul@example.com",
    "created_at": "2025-01-15T10:30:00Z",
    "transactions": [...]
  }
]
```

#### **POST /api/customers/**
Create a new customer

**Request Body:**
```json
{
  "name": "Priya Singh",
  "phone": "+919876543211",
  "email": "priya@example.com"  // optional
}
```

**Response:**
```json
{
  "id": 2,
  "name": "Priya Singh",
  "phone": "+919876543211",
  "email": "priya@example.com",
  "created_at": "2025-01-20T14:20:00Z",
  "transactions": []
}
```

#### **GET /api/customers/{id}/**
Get single customer details

#### **PUT /api/customers/{id}/**
Update customer details

#### **DELETE /api/customers/{id}/**
Delete a customer

---

### 2. **Transaction Recording**

#### **POST /api/record_transaction/**
Record a new credit or debit transaction

**Request Body (multipart/form-data):**
```json
{
  "customer_id": 1,
  "transaction_type": "credit",  // or "debit"
  "amount": "5000.00",
  "proof_image": <file>  // optional image file
}
```

**Response:**
```json
{
  "success": true,
  "balance": "5000.00",
  "message": "Transaction recorded successfully"
}
```

**Business Logic:**
- Credit: Increases customer balance (they owe you)
- Debit: Decreases balance (payment received)
- Automatically calculates running balance
- Sends SMS notification for:
  - All credit transactions
  - Debit transactions that clear balance (balance = 0)

**SMS Format:**
```
Hello Rahul Sharma,
₹5000 added to your Khata
Balance: ₹5000
View full Khata: http://localhost:5174/statement/1
```

---

### 3. **Customer Statement**

#### **GET /api/statement/{customer_id}/**
Get complete transaction history for a customer

**Response:**
```json
{
  "customer": "Rahul Sharma",
  "phone": "+919876543210",
  "transactions": [
    {
      "date": "2025-01-15T10:30:00Z",
      "type": "credit",
      "amount": "5000.00",
      "balance": "5000.00",
      "proof_image": "http://localhost:8000/media/transaction_proofs/image1.jpg"
    },
    {
      "date": "2025-01-16T11:00:00Z",
      "type": "debit",
      "amount": "2000.00",
      "balance": "3000.00",
      "proof_image": null
    }
  ]
}
```

---

### 4. **Send Reminder**

#### **GET or POST /api/send-reminder/{customer_id}/**
Manually send SMS reminder to customer with pending dues

**Response:**
```json
{
  "success": true,
  "message": "Reminder sent",
  "sms_info": {...}
}
```

**Error Cases:**
```json
{
  "error": "No pending balance to remind"
}
```

**SMS Format:**
```
Hello Rahul Sharma,
Pending amount: ₹3000
Please clear your due at the earliest.
- Khata App
```

---

## 📊 Data Models & Structure

### 1. **Customer Model**
```python
{
  "id": Integer (Primary Key),
  "name": String (max 200 chars),
  "phone": String (max 20 chars),
  "email": String (optional),
  "created_at": DateTime
}
```

### 2. **Transaction Model**
```python
{
  "id": Integer (Primary Key),
  "customer": Foreign Key -> Customer,
  "amount": Decimal (10, 2),
  "transaction_type": Choice["credit", "debit"],
  "balance_after": Decimal (10, 2),
  "note": String (max 255, optional),
  "proof_image": ImageField (optional),
  "created_at": DateTime
}
```

### 3. **Reminder Model** (Currently not used in views, but exists)
```python
{
  "id": Integer (Primary Key),
  "customer": Foreign Key -> Customer,
  "amount": Decimal,
  "due_date": DateTime,
  "message": Text,
  "status": Choice["pending", "sent", "paid"],
  "created_at": DateTime,
  "last_sent_at": DateTime (optional)
}
```

---

## 💻 Frontend Requirements

### Technology Stack Recommendations
- **Framework:** React.js (Vite) - Already set up at `localhost:5173`
- **Routing:** React Router v6
- **State Management:** React Context API or Redux Toolkit
- **HTTP Client:** Axios
- **UI Library:** Material-UI, Ant Design, or Chakra UI
- **Form Handling:** React Hook Form
- **Date Handling:** Day.js or date-fns
- **Icons:** React Icons or Lucide React
- **Toast Notifications:** React Hot Toast or Sonner

### Key Frontend Features Needed
1. ✅ Customer CRUD operations
2. ✅ Transaction recording with image upload
3. ✅ Real-time balance display
4. ✅ Statement view with transaction history
5. ✅ Search & filter customers
6. ✅ SMS reminder trigger
7. ✅ Responsive design (mobile-first)
8. ✅ Image proof viewer
9. ✅ Dashboard with statistics

---

## 🎨 Pages & Components Specification

### **1. Dashboard / Home Page** (`/`)

**Purpose:** Overview of business metrics and quick actions

**Components Needed:**
- **Summary Cards:**
  - Total Customers
  - Total Outstanding Amount (sum of all positive balances)
  - Total Transactions Today
  - Total Given Credit This Month

- **Recent Transactions List:**
  - Last 10 transactions across all customers
  - Show: Customer name, amount, type, timestamp
  - Click to view customer statement

- **Quick Actions:**
  - Add New Customer (button)
  - Record Transaction (button)

**UI Elements:**
```
┌─────────────────────────────────────────┐
│  📊 Dashboard                            │
├─────────────────────────────────────────┤
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐   │
│  │ 150 │  │ ₹45K│  │ 25  │  │ ₹12K│   │
│  │Cust │  │Dues │  │Today│  │Month│   │
│  └─────┘  └─────┘  └─────┘  └─────┘   │
│                                         │
│  Recent Transactions                    │
│  ┌─────────────────────────────────┐  │
│  │ Rahul +₹5000  [10:30 AM]        │  │
│  │ Priya -₹2000  [11:15 AM]        │  │
│  └─────────────────────────────────┘  │
│                                         │
│  [+ Add Customer] [+ Record Transaction]│
└─────────────────────────────────────────┘
```

---

### **2. Customers List Page** (`/customers`)

**Purpose:** View and manage all customers

**Components:**
- **Search Bar:**
  - Search by name or phone number
  - Real-time filtering

- **Filter Options:**
  - All Customers
  - With Pending Dues (balance > 0)
  - Cleared (balance = 0)
  - Sort by: Name, Balance, Recent Activity

- **Customer Cards/List:**
  - Customer name
  - Phone number
  - Current balance (color-coded: red if > 0, green if 0)
  - Last transaction date
  - Action buttons: View Statement, Add Transaction, Send Reminder

- **Add Customer Button:** Fixed/floating button

**UI Elements:**
```
┌─────────────────────────────────────────┐
│  👥 Customers                [+ Add]     │
├─────────────────────────────────────────┤
│  [Search..............................]  │
│  [All] [Pending] [Cleared] [Sort ▼]     │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ Rahul Sharma          Balance: ₹3K │ │
│  │ +91-9876543210                     │ │
│  │ Last: 2 days ago                   │ │
│  │ [View] [Add ₹] [📱 Remind]        │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ Priya Singh           Balance: ₹0  │ │
│  │ +91-9876543211                     │ │
│  │ Last: 5 days ago                   │ │
│  │ [View] [Add ₹]                     │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**Functionality:**
- Click customer card → Navigate to statement page
- "Add ₹" → Open transaction modal
- "Remind" → Send SMS reminder (disabled if balance = 0)

---

### **3. Add/Edit Customer Page** (`/customers/new`, `/customers/:id/edit`)

**Purpose:** Create or edit customer details

**Form Fields:**
- Name* (required)
- Phone Number* (required, validate 10 digits)
- Email (optional)

**Validation:**
- Name: min 2 characters
- Phone: exactly 10 digits, no duplicates
- Email: valid email format

**UI Elements:**
```
┌─────────────────────────────────────────┐
│  ← Add New Customer                      │
├─────────────────────────────────────────┤
│  Name *                                  │
│  [...................................]   │
│                                          │
│  Phone Number *                          │
│  [+91] [.....................]           │
│                                          │
│  Email (optional)                        │
│  [...................................]   │
│                                          │
│  [Cancel]              [Save Customer]   │
└─────────────────────────────────────────┘
```

---

### **4. Add Transaction Page/Modal** (`/transactions/new` or Modal)

**Purpose:** Record credit or debit transaction

**Form Fields:**
- Select Customer* (dropdown/search)
- Transaction Type* (Credit / Debit)
- Amount* (number, min 0.01)
- Upload Proof (optional image)
- Note (optional, max 255 chars)

**UI Elements:**
```
┌─────────────────────────────────────────┐
│  ← Record Transaction                    │
├─────────────────────────────────────────┤
│  Customer *                              │
│  [Select Customer ▼]                     │
│                                          │
│  Transaction Type *                      │
│  ( ) Credit (Given)  ( ) Debit (Received)│
│                                          │
│  Amount *                                │
│  ₹ [.......................]             │
│                                          │
│  Upload Proof (Optional)                 │
│  [📎 Choose File]                        │
│  [Preview if uploaded]                   │
│                                          │
│  Note (Optional)                         │
│  [...................................]   │
│                                          │
│  Current Balance: ₹3,000                 │
│  New Balance: ₹5,000 (if credit ₹2000)  │
│                                          │
│  [Cancel]              [Record ✓]        │
└─────────────────────────────────────────┘
```

**Functionality:**
- Real-time balance calculation preview
- Image preview after upload
- Confirmation dialog before submitting
- Success toast: "Transaction recorded! SMS sent to customer"

---

### **5. Customer Statement Page** (`/statement/:customer_id`)

**Purpose:** Detailed transaction history for a customer

**Components:**
- **Customer Header:**
  - Name, phone
  - Current balance (large, prominent)
  - Action buttons: Add Transaction, Send Reminder, Export PDF

- **Transaction Timeline:**
  - Chronological list (newest first)
  - Each transaction shows:
    - Date & time
    - Type (Credit/Debit with icon)
    - Amount
    - Balance after transaction
    - Proof image thumbnail (click to view full)
    - Note (if any)

- **Summary Section:**
  - Total Credit Given
  - Total Payments Received
  - Net Balance

**UI Elements:**
```
┌─────────────────────────────────────────┐
│  ← Rahul Sharma                          │
│     +91-9876543210                       │
│                                          │
│     Current Balance                      │
│     ₹ 3,000                              │
│                                          │
│  [+ Add Transaction] [📱 Send Reminder]  │
├─────────────────────────────────────────┤
│  Transaction History                     │
│                                          │
│  📅 Jan 16, 2025 - 11:00 AM             │
│  💸 Payment Received                     │
│  ₹ 2,000                                 │
│  Balance: ₹3,000                         │
│  [📷 View Proof]                         │
│  ──────────────────────────              │
│                                          │
│  📅 Jan 15, 2025 - 10:30 AM             │
│  📤 Credit Given                         │
│  ₹ 5,000                                 │
│  Balance: ₹5,000                         │
│  Note: "Monthly supplies"                │
│  ──────────────────────────              │
│                                          │
│  Summary                                 │
│  Total Credit:   ₹ 5,000                 │
│  Total Received: ₹ 2,000                 │
│  Net Balance:    ₹ 3,000                 │
└─────────────────────────────────────────┘
```

**Functionality:**
- Click proof thumbnail → Open lightbox/modal with full image
- Send Reminder → Show confirmation, then send SMS
- Export PDF → Generate downloadable statement (future feature)

---

### **6. Common Components**

#### **Navbar/Header**
- App logo/name
- Navigation links: Dashboard, Customers
- User profile (if auth added later)

#### **Transaction Card Component**
Reusable component for displaying transaction

#### **Customer Card Component**
Reusable component for customer list

#### **Image Viewer Modal**
For viewing transaction proof images

#### **Confirmation Dialog**
For delete/reminder actions

#### **Loading States**
Skeleton loaders for all data fetching

#### **Empty States**
When no customers or transactions exist

---

## 🎨 UI/UX Design Guidelines

### Color Scheme
```css
/* Primary Colors */
--primary: #4F46E5 (Indigo)
--secondary: #10B981 (Green)
--danger: #EF4444 (Red)
--warning: #F59E0B (Amber)

/* Backgrounds */
--bg-primary: #FFFFFF
--bg-secondary: #F9FAFB
--bg-card: #FFFFFF

/* Text */
--text-primary: #111827
--text-secondary: #6B7280
--text-muted: #9CA3AF

/* Balance Colors */
--balance-positive: #DC2626 (Red - they owe you)
--balance-zero: #10B981 (Green - cleared)
```

### Typography
- **Headings:** Inter, SF Pro, or Poppins (Bold)
- **Body:** Inter or SF Pro (Regular)
- **Numbers:** Tabular nums for balance alignment

### Transaction Type Visual Indicators
- **Credit (Given):** 📤 or ↑ with red/orange color
- **Debit (Received):** 💸 or ↓ with green color

### Mobile First Design
- Stack cards vertically on mobile
- Bottom navigation for main actions
- Swipe gestures for quick actions
- Large touch targets (min 44px)

### Accessibility
- Proper contrast ratios (WCAG AA)
- Screen reader labels
- Keyboard navigation
- Focus indicators

---

## 🔗 Integration Guide

### 1. **Axios Setup**

```javascript
// src/api/axios.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
  headers: {
    'Content-Type': 'application/json',
  },
});

// For file uploads
export const uploadAPI = axios.create({
  baseURL: 'http://localhost:8000/api/',
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

export default api;
```

### 2. **API Service Functions**

```javascript
// src/services/customerService.js
import api from '../api/axios';

export const customerService = {
  // Get all customers
  getAll: () => api.get('/customers/'),
  
  // Get single customer
  getById: (id) => api.get(`/customers/${id}/`),
  
  // Create customer
  create: (data) => api.post('/customers/', data),
  
  // Update customer
  update: (id, data) => api.put(`/customers/${id}/`, data),
  
  // Delete customer
  delete: (id) => api.delete(`/customers/${id}/`),
  
  // Get statement
  getStatement: (id) => api.get(`/statement/${id}/`),
  
  // Send reminder
  sendReminder: (id) => api.post(`/send-reminder/${id}/`),
};
```

```javascript
// src/services/transactionService.js
import { uploadAPI } from '../api/axios';

export const transactionService = {
  create: (data) => {
    const formData = new FormData();
    formData.append('customer_id', data.customer_id);
    formData.append('transaction_type', data.transaction_type);
    formData.append('amount', data.amount);
    
    if (data.proof_image) {
      formData.append('proof_image', data.proof_image);
    }
    
    return uploadAPI.post('/record_transaction/', formData);
  },
};
```

### 3. **Context/State Management Example**

```javascript
// src/context/CustomerContext.jsx
import { createContext, useState, useEffect } from 'react';
import { customerService } from '../services/customerService';

export const CustomerContext = createContext();

export const CustomerProvider = ({ children }) => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchCustomers = async () => {
    setLoading(true);
    try {
      const response = await customerService.getAll();
      setCustomers(response.data);
    } catch (error) {
      console.error('Error fetching customers:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCustomers();
  }, []);

  return (
    <CustomerContext.Provider value={{ customers, loading, fetchCustomers }}>
      {children}
    </CustomerContext.Provider>
  );
};
```

### 4. **Routing Setup**

```javascript
// src/App.jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import CustomerList from './pages/CustomerList';
import AddCustomer from './pages/AddCustomer';
import Statement from './pages/Statement';
import AddTransaction from './pages/AddTransaction';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/customers" element={<CustomerList />} />
        <Route path="/customers/new" element={<AddCustomer />} />
        <Route path="/customers/:id/edit" element={<AddCustomer />} />
        <Route path="/statement/:id" element={<Statement />} />
        <Route path="/transactions/new" element={<AddTransaction />} />
      </Routes>
    </BrowserRouter>
  );
}
```

### 5. **Error Handling**

```javascript
// src/utils/errorHandler.js
import toast from 'react-hot-toast';

export const handleAPIError = (error) => {
  if (error.response) {
    // Server responded with error
    const message = error.response.data.error || 'Something went wrong';
    toast.error(message);
  } else if (error.request) {
    // Request made but no response
    toast.error('Network error. Please check your connection.');
  } else {
    // Something else happened
    toast.error('An unexpected error occurred.');
  }
  
  console.error('API Error:', error);
};
```

---
