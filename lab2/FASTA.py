

def ReadFASTA(data_location):
        if type(data_location) == list:
                fasta_list =[]
                for location in data_location:
                        fasta_list+=ReadFASTA(location)
                return fasta_list


        if data_location[-4:] == '.txt':
                with open(data_location) as f:
                        return ParseFASTA(f)

def ParseFASTA(f):
        fasta_list=[]
        for line in f:

                if line[0] == '>':


                        try:
                                fasta_list.append(current_dna)
                        except UnboundLocalError:
                                pass

                        current_dna = [line.lstrip('>').rstrip('\n'),'']

                else:
                        current_dna[1] += line.rstrip('\n')

        fasta_list.append(current_dna)

        return fasta_list