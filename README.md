# 📚 Book Scraper — Readings.com Book Extractor with Search & Sort

**Book Scraper** is a Python + PyQt5 application that automatically scrapes book data from [Readings.com](https://www.readings.com/) and provides a clean, interactive interface for managing the extracted information.

You can specify any **category URL** (e.g., fiction, biography, history, etc.), set a **page limit**, and scrape all book data at once.  
After scraping, you can **load**, **search**, and **sort** the data — including **multi-level sorting** for advanced organization.

---

## 🌟 Features

✅ **Category-based Scraping**  
- Works on *any* category URL from [Readings.com](https://www.readings.com/).  
- Example: Fiction, Non-Fiction, History, Art, or Children’s books.  
- You can set a custom **page limit** before scraping begins.

✅ **Automated Data Extraction**  
- Uses `Selenium` and `BeautifulSoup` to scrape book details (title, author, price, and more).  
- Extracted data is stored in CSV format for easy reuse.

✅ **Interactive GUI (PyQt5)**  
- Built with `PyQt5` for a modern, responsive interface.  
- **Start Button:** begins scraping process.  
- **Load Button:** loads previously extracted data instantly.

✅ **Search & Sort Tools**  
- Perform **simple** and **multi-level** sorting (e.g., sort by author, then price).  
- Apply **keyword search** to filter books by title, author, or price range.  
- Real-time updates inside the table view.

✅ **Multi-level Sorting & Searching**  
- Combine multiple sort conditions for complex datasets.  
- Case-insensitive search with instant filtering.

✅ **Progress Feedback**  
- Live progress updates during scraping (page count, total items, etc.).

---

## 🧰 Technologies Used

| Component | Technology |
|------------|-------------|
| Language | Python 3 |
| GUI Framework | PyQt5 |
| Web Scraping | Selenium, BeautifulSoup4 |
| Data Handling | Pandas |
| Output | CSV |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/book-scraper.git
cd book-scraper
