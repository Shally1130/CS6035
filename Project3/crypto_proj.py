import hashlib
import json
import math
import os
import random
# You may NOT alter the import list!!!!
# activate python3

class CryptoProject(object):

    def __init__(self):
        # TODO: Change this to YOUR Georgia Tech student ID!!!
        # Note that this is NOT your 9-digit Georgia Tech ID
        self.student_id = 'dgoodrick3'

    def get_student_id_hash(self):
        return hashlib.sha224(self.student_id.encode('UTF-8')).hexdigest()

    def get_all_data_from_json(self, filename):
        data = None
        base_dir = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(base_dir, filename), 'r') as f:
            data = json.load(f)
        return data
        # base_dir = os.getcwd()
        # with open(os.path.join(base_dir, filename), 'r') as f:
            # data = json.load(f)
        # return data

    def get_data_from_json_for_student(self, filename):
        data = self.get_all_data_from_json(filename)
        name = self.get_student_id_hash()
        if name not in data:
            print(self.student_id + ' not in file ' + filename)
            return None
        else:
            return data[name]

    # TODO: OPTIONAL - Add helper functions below
    # BEGIN HELPER FUNCTIONS
        
    def extendedEuclidian(self, e, tot_n):
        #https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Python
        if e == 0:
            #Stop once the remainder of big%small is 0
            #big is the GCD
            return (tot_n, 0, 1)
        else:
            #break down the multiples by dividing the previous big number by it's remainder
            gcd, k, a = self.extendedEuclidian(tot_n % e, e)
            # substitute back in k and multiples of N to get d=a-k(N//rem)
            return gcd, a - k*(tot_n // e), k
        
    def mod_inv(self,e, tot_n):
        #https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Python
        gcd,raw,_ = self.extendedEuclidian(e, tot_n)
        if gcd==1:  #GCD must be one or there is no solution
            return raw%tot_n #ensures the result is positive
        return 'NaN'
    
    def binarySearch(self,val):
        # https://rosettacode.org/wiki/Binary_search#Python:_Iterative
        lower=0
        upper = val
        while lower < upper:
            mid = (lower+upper)//2
            if mid**3 < val:
                lower = mid+1
            else:
                upper = mid
        return lower
    
    # END HELPER FUNCTIONS

    def decrypt_message(self, N, e, d, c):
        # https://en.wikipedia.org/wiki/RSA_(cryptosystem)
        return hex(pow(c,d,N))

    def crack_password_hash(self, password_hash, weak_password_list):
        password = 'abc'
        salt = '123'
        for password in weak_password_list:
            for salt in weak_password_list:
                hashed_password = hashlib.sha256(password.encode() + salt.encode()).hexdigest()
                if hashed_password == password_hash:
                    print("PWD:", password, "Salt:", salt)
                    return password, salt
        
        return "not found"

    def get_factors(self, n):
        #check all odd values > sqrt(n) because p or q must be > Sqrt(n)  
        start = 2*(n**.5//2)-1
        for i in range(int(start),n,2):
            if n%i == 0:
                return i, n//i
        return 'NaN', 'NaN'

    def get_private_key_from_p_q_e(self, p, q, e):
        # TODO: Implement this function for Task 3
        # e*d≡1 mod ϕ(N) 
        # ϕ(N)=ϕ(p)ϕ(q)=(p−1)(q−1)
        # extendedEuclidian takes ϕ(N) and e and returns d such that ed+kϕ(N)=1  
        tot = (p-1)*(q-1)
        return self.mod_inv(e, tot)
        
    def is_waldo(self, n1, n2):
        # TODO: Implement this function for Task 4
        '''The greatest common divisor (GCD) of two 1024-bit integers
            can be computed in microseconds. Find two distinct RSA moduli 
            N1 and N2 that share a prime factor...'''
        if math.gcd(n1,n2) != 1:
            return True
        else:
            return False

    def get_private_key_from_n1_n2_e(self, n1, n2, e):
        # TODO: Implement this function for Task 4
        # assumption: n1 and n2 share a common factor
        # The GCD of N1 and N2 is p        
        p = math.gcd(n1, n2)
        # n2/p = q2 but we only want the private key, d, of n1 so q2 doesn't matter 
        q = n1//p
        tot = (p-1)*(q-1)
        #private key d satisfies de = 1 mod (p-1)(q-1):
        return self.mod_inv(e, tot )
        

    def recover_msg(self, N1, N2, N3, C1, C2, C3):
        # TODO: Implement this function for Task 5
        C = [C1, C2, C3]
        N = [N1,N2, N3]
        #find the n that doesn't include Ni
        n = [N2*N3,N1*N3,N1*N2]# I could have used [pN/N1, pN/N2, pN/N3]
        x = [self.mod_inv(n[i],N[i]) for i in range(len(C))]
        c = [n[i]*C[i]*x[i] for i in range(len(C))]
        s = sum(c)
        pN =N1*N2*N3
        ans = s%pN
        return self.binarySearch(ans)       

    def task_1(self):
        data = self.get_data_from_json_for_student('keys4student_task_1.json')
        N = int(data['N'], 16)
        e = int(data['e'], 16)
        d = int(data['d'], 16)
        c = int(data['c'], 16)
        self.data = data
        m = self.decrypt_message(N, e, d, c)
        return m

    def task_2(self):
        data = self.get_data_from_json_for_student('hashes4student_task_2.json')
        password_hash = data['password_hash']
        self.data = data

        # The password file is loaded as a convenience
        weak_password_list = []
#         base_dir = os.path.abspath(os.path.dirname(__file__))
        base_dir = os.getcwd()
        with open(os.path.join(base_dir, 'top_passwords.txt'), 'r', encoding='UTF-8-SIG') as f:
            pw = f.readline()
            while pw:
                weak_password_list.append(pw.strip('\n'))
                pw = f.readline()
        self.ph = password_hash
        self.wp = weak_password_list
        password, salt = self.crack_password_hash(password_hash, weak_password_list)

        return password, salt

    def task_3(self):
        data = self.get_data_from_json_for_student('keys4student_task_3.json')
        n = int(data['N'], 16)
        e = int(data['e'], 16)

        p, q = self.get_factors(n)
        d = self.get_private_key_from_p_q_e(p, q, e)

        return hex(d).rstrip('L')

    def task_4(self):
        all_data = self.get_all_data_from_json('keys4student_task_4.json')
        student_data = self.get_data_from_json_for_student('keys4student_task_4.json')
        n1 = int(student_data['N'], 16)
        e = int(student_data['e'], 16)

        d = 0
        waldo = 'Dolores'

        for classmate in all_data:
            if classmate == self.get_student_id_hash():
                continue
            n2 = int(all_data[classmate]['N'], 16)

            if self.is_waldo(n1, n2):
                waldo = classmate
                #print(bin(n2))
                d = self.get_private_key_from_n1_n2_e(n1, n2, e)
                break

        return hex(d).rstrip("L"), waldo

    def task_5(self):
        data = self.get_data_from_json_for_student('keys4student_task_5.json')
        N1 = int(data['N0'], 16)
        N2 = int(data['N1'], 16)
        N3 = int(data['N2'], 16)
        C1 = int(data['C0'], 16)
        C2 = int(data['C1'], 16)
        C3 = int(data['C2'], 16)
        
        m = self.recover_msg(N1, N2, N3, C1, C2, C3)
        # Convert the int to a message string
        msg = bytes.fromhex(hex(m).rstrip('L')[2:]).decode('UTF-8')

        return msg


if __name__ == '__main__':

    cp = CryptoProject()
    cp.task_1()
    cp.task_2()
    cp.task_3()
    cp.task_4()
    cp.task_5()