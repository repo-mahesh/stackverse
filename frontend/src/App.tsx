import { useEffect, useState } from "react";
import axios from "axios";


interface Tag {
  id: number;
  name: string;
}

interface Quote {
  id: number;
  content: string;
  author: string;
  source?: string;  // Optional field with '?'
  tags: Tag[];
}

const DailyQuotes = () => {
  const [quotes, setQuotes] = useState<Quote[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch daily quotes
    const fetchQuotes = async () => {
      try {
        const response = await axios.get<Quote[]>("http://127.0.0.1:8000/api/daily-quotes/");
        setQuotes(response.data);
      } catch (error) {
        console.error("Error fetching quotes:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchQuotes();
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      <h1>Daily Quotes</h1>
      {quotes.map((quote: Quote) => (
        <div key={quote.id}>
          <blockquote>{quote.content}</blockquote>
          <p>- {quote.author}</p>
          {quote.source && <p>Source: {quote.source}</p>}
          <p>Tags: {quote.tags.map(tag => tag.name).join(', ')}</p>
        </div>
      ))}
    </div>
  );
};

export default DailyQuotes;