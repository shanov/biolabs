import java.util.Hashtable;

public class Main {

    // Состояние
    static final String HEALTHY = "Healthy";
    static final String ILL = "Ill";

    // Внешний вид
    static final String BAD = "Bad";
    static final String MEDIUM = "Medium";
    static final String GOOD = "Good";

    public static void main(String[] args) {
        String[] states = new String[] {HEALTHY, ILL};

        String[] observations = new String[] {BAD, MEDIUM, GOOD};

        Hashtable<String, Float> start_probability = new Hashtable<String, Float>();
        start_probability.put(HEALTHY, 0.6f);
        start_probability.put(ILL, 0.4f);

        // Начальное состояние
        Hashtable<String, Hashtable<String, Float>> transition_probability =
                new Hashtable<String, Hashtable<String, Float>>();
        Hashtable<String, Float> t1 = new Hashtable<String, Float>();
        t1.put(HEALTHY, 0.6f);
        t1.put(ILL, 0.4f);
        Hashtable<String, Float> t2 = new Hashtable<String, Float>();
        t2.put(HEALTHY, 0.2f);
        t2.put(ILL, 0.8f);
        transition_probability.put(HEALTHY, t1);
        transition_probability.put(ILL, t2);

        // Вероятность переходов
        Hashtable<String, Hashtable<String, Float>> emission_probability =
                new Hashtable<String, Hashtable<String, Float>>();
        Hashtable<String, Float> e1 = new Hashtable<String, Float>();
        e1.put(BAD, 0.5f);
        e1.put(MEDIUM, 0.3f);
        e1.put(GOOD, 0.2f);
        Hashtable<String, Float> e2 = new Hashtable<String, Float>();
        e2.put(BAD, 0.2f);
        e2.put(MEDIUM, 0.3f);
        e2.put(GOOD, 0.5f);
        emission_probability.put(HEALTHY, e1);
        emission_probability.put(ILL, e2);

        Object[] ret = forward_viterbi(observations,
                states,
                start_probability,
                transition_probability,
                emission_probability);
        System.out.println(((Float) ret[0]).floatValue());
        System.out.println((String) ret[1]);
        System.out.println(((Float) ret[2]).floatValue());
    }

    public static Object[] forward_viterbi(String[] obs, String[] states,
                                           Hashtable<String, Float> start_p,
                                           Hashtable<String, Hashtable<String, Float>> trans_p,
                                           Hashtable<String, Hashtable<String, Float>> emit_p)
    {
        Hashtable<String, Object[]> T = new Hashtable<String, Object[]>();
        for (String state : states)
            T.put(state, new Object[] {start_p.get(state), state, start_p.get(state)});

        for (String output : obs)
        {
            Hashtable<String, Object[]> U = new Hashtable<String, Object[]>();
            for (String next_state : states)
            {
                float total = 0;
                String argmax = "";
                float valmax = 0;

                float prob = 1;
                String v_path = "";
                float v_prob = 1;

                for (String source_state : states)
                {
                    Object[] objs = T.get(source_state);
                    prob = ((Float) objs[0]).floatValue();
                    v_path = (String) objs[1];
                    v_prob = ((Float) objs[2]).floatValue();

                    float p = emit_p.get(source_state).get(output) *
                            trans_p.get(source_state).get(next_state);
                    prob *= p;
                    v_prob *= p;
                    total += prob;
                    if (v_prob > valmax)
                    {
                        argmax = v_path + "," + next_state;
                        valmax = v_prob;
                    }
                }
                U.put(next_state, new Object[] {total, argmax, valmax});
            }
            T = U;
        }

        float total = 0;
        String argmax = "";
        float valmax = 0;

        float prob;
        String v_path;
        float v_prob;

        for (String state : states)
        {
            Object[] objs = T.get(state);
            prob = ((Float) objs[0]).floatValue();
            v_path = (String) objs[1];
            v_prob = ((Float) objs[2]).floatValue();
            total += prob;
            if (v_prob > valmax)
            {
                argmax = v_path;
                valmax = v_prob;
            }
        }
        return new Object[]{total, argmax, valmax};
    }
}
