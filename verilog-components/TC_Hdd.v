module TC_Hdd (clk, rst, seek, load, save, in, out);
    parameter MEM_WORDS = 256;
    parameter HEX_FILE = "test_jumps.mem";
    parameter ARG_SIG = "HEX_FILE=%s";
    reg [1024*8:0] hexfile;
    input clk;
    input rst;
    input [63:0] seek;
    input load;
    input save;
    input [63:0] in;
    output [63:0] out;
    
    reg [63:0] mem [0:MEM_WORDS-1];
    reg [63:0] outval;
    reg [63:0] mp;
    
    initial begin
        hexfile <= HEX_FILE;
        if ($value$plusargs(ARG_SIG, hexfile)) begin
            $display("loading %0s", hexfile);
            $readmemh(hexfile, mem);
        end else begin
            $display("no file specified");
        end
    end

    always @ (posedge clk or rst) begin
        if (rst) begin
            mp = {64{1'bZ}};
            outval = {64{1'bZ}};
        end else begin
            mp <= mp + seek;
            if (load) begin
                outval <= mem[mp];
            end
        end
    end
    
    always @ (posedge clk or rst) begin
        if (save && !rst) begin
            mem[mp] <= in;
        end
    end
    
    assign out = outval;
endmodule
