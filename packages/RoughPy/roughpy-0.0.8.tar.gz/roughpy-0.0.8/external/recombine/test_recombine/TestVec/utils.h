#ifndef utils_h__
#define utils_h__

inline doublereal dUniformRandomVariable(const doublereal lower=doublereal(-1.), const doublereal upper = doublereal(1.))
{
	// returns a uniform random variable on the interval [lower, upper]
	return lower + (upper - lower) * ((doublereal)rand()) / ((doublereal)RAND_MAX);
}

template <class T>
std::ostream& operator <<(std::ostream& os, const std::vector<T>& in)
{
	os << "{";
	for (typename std::vector<T>::const_iterator it(in.begin()); it != in.end(); ++it)
	{
		os << *it;
		if (it + 1 != in.end())
			os << ", ";
	}
	os << "}";
	return os;
}

class my_seed {
    std::vector<uint32_t> entropy_vector;
    std::seed_seq seed_sequence;

    static std::vector<uint32_t> make_entropy_vector()
    {
        std::vector<uint32_t> entropy_vector;
        std::random_device en;
        for (uint32_t i = 0; i<32; ++i)
            entropy_vector.push_back(en());
        return entropy_vector;
    }

    my_seed()
            :
            entropy_vector(make_entropy_vector()),
            seed_sequence(begin(entropy_vector), end(entropy_vector))
    {
        entropy_vector.clear();
    }

    const std::seed_seq& operator()() const { return seed_sequence; }

public:

    friend const std::seed_seq& get_seed()
    {
        static my_seed shared_seed;
        return shared_seed();
    }
};
#endif // utils_h__
