const LanguageSelector = () => {
    return (
        <select className="mb-4 border p-2">
            <option value="en">English</option>
            <option value="hi">Hindi</option>
            <option value="ta">Tamil</option>
            <option value="te">Telugu</option>
            {/* Add more languages as needed */}
        </select>
    );
};

export default LanguageSelector;
